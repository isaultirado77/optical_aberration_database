from yaml import safe_load, safe_dump
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
from tqdm import tqdm
from src.aberrations import (
    generate_interferogram, 
    add_gaussian_noise, 
    add_poisson_noise, 
    add_dust_particles, 
    add_random_motion_blur, 
    save_as_tiff
)
from src.metrics import (
    calculate_statistics, 
    calculate_haralick_features, 
    calculate_wavefront_error, 
    calculate_image_quality_metrics
)

@dataclass
class AberrationConfig:
    name = str
    coefficients: List[Tuple[int, int, float, float]]  # (n, m, min, max)
    samples: int
    noise: Dict[str, bool]

class DatasetGenerator: 
    def __init__(self, config_path: Path, print_config: bool = False):
        self.config = self._load_config(config_path)
        self.rng = np.random.default_rng(self.config['metadata'].get("seed", 42))  # Generador de números aleatorios con semilla fija (para reproducibilidad).
        if print_config: 
            self._print_config()
        p = self.config["noise_profiles"]["default_gaussian"]
        print(p['sigma_percent'], p['clip'])

    def _load_config(self, path: Path) -> Dict: 
        with open(path) as f: 
            config = safe_load(f)
        
        # Validar estructura
        required_sections = {"metadata", "optical_parameters", "noise_profiles", "classes"}
        if not required_sections.issubset(config.keys()): 
            raise ValueError(f"Config file missing required sections: {required_sections - config.keys()}")
            
        return config
    
    def _print_config(self):
        def print_dict(d: Dict, indent: int = 0):
            for key, value in d.items():
                print(" " * indent + f"{key}:")
                if isinstance(value, dict):
                    print_dict(value, indent + 2)
                else:
                    print(" " * (indent + 2) + str(value))

        print("CONFIG:")
        print_dict(self.config)
    
    def _generate_coefficients(self, aberration: Dict) -> Dict[Tuple[int, int], float]:
        """Genera coeficientes aleatorios basados según la configuración."""
        return {
            (n, m): self.rng.uniform(low, high)
            for n, m, low, high in aberration["coefficients"]
        }

    def _apply_noises(self, image: np.ndarray, noise_config: Dict[str, bool]) -> np.ndarray:
        """Aplica ruidos según la configuración"""
        # Gaussian
        if noise_config.get("gaussian", False):
            params = self.config["noise_profiles"]["default_gaussian"]
            sigma = params.get('sigma_percent', 0.5)
            clip = params.get('clip', True)
            image = add_gaussian_noise(image, sigma, clip)
            
        # Poisson
        if noise_config.get("poisson", False):
            params = self.config["noise_profiles"]["default_poisson"]
            scale = params.get('scale', 1000)
            normalize = params.get('normalize', True)
            image = add_poisson_noise(image, scale, normalize)
            
        # Dust
        if noise_config.get("dust", False):
            params = self.config["noise_profiles"]["default_dust"]
            num_particles = params.get('num_particles', (2, 5))
            max_radius = params.get('max_radius', 15)
            intensity = params.get('intensity', 0.0)
            image = add_dust_particles(image, num_particles, max_radius, intensity)
            
        # Vibration
        if noise_config.get("vibration", False):
            params = self.config["noise_profiles"]["default_vibration"]
            max_kernel_size = params.get('max_kernel_size', 21)
            intensity = params.get('intensity', 1.0)
            image = add_random_motion_blur(image, max_kernel_size, intensity)
            
        return image


    def generate_dataset(self, output_dir: Path):
        """Genera el dataset completo"""
        output_dir.mkdir(parents=True, exist_ok=True)
        metrics_data = []
        
        # Directorios de salida
        raw_dir = output_dir / "raw"
        raw_dir.mkdir(exist_ok=True)
        
        # Generar imágenes para cada clase
        for class_name, class_config in tqdm(
            self.config["classes"].items(),
            desc="Generando clases de aberración"
        ):
            for i in tqdm(range(class_config["samples"]), desc=f"Clase {class_name}", leave=False):
                # 1. Generar coeficientes
                coefficients = self._generate_coefficients(class_config)
                
                # 2. Crear interferograma
                interferogram = generate_interferogram(
                    coefficients,
                    shape=(
                        self.config["metadata"].get("image_height", 512),
                        self.config["metadata"].get("image_width", 512)
                    )
                )
                
                # 3. Aplicar ruidos
                noisy_interferogram = self._apply_noises(interferogram, class_config.get("noise", {}))
                
                # 4. Guardar imagen
                image_id = f"{class_name}_{i:04d}"
                save_as_tiff(
                    interferogram,
                    raw_dir / f"{image_id}.tiff",
                )

                # 5. Generar métricas
                metrics = self._extract_data(interferogram, noisy_interferogram, coefficients)

                # 6. Registrar métricas
                metrics_data.append({
                    "image_id": image_id, 
                    "class": class_name, 
                    **metrics
                })
        
        # Guardar datos y métricas
        self._save_metadata(output_dir)
        pd.DataFrame(metrics_data).to_csv(output_dir / "metrics.csv")

    def _extract_data(self,
                      interferogram: np.ndarray,
                      noisy_interferogram: np.ndarray,
                      coefficients: Dict[Tuple[int, int], float]) -> Dict:
        """Extrae todas las métricas y coeficientes para guardar en CSV"""

        intems_view = coefficients.items()
        interator = iter(intems_view)
        tuple_pair = next(interator)
        (n, m), coeff = tuple_pair  # usar next(iter(coefficients.items()))
        stats = calculate_statistics(interferogram)
        wavefront_metrics = calculate_wavefront_error(interferogram)
        texture_metrics = calculate_haralick_features(interferogram)
        quality_metrics = calculate_image_quality_metrics(interferogram, noisy_interferogram)
  
        # Combinar todos los datos
        return {
            'n': n,
            'm': m,
            'coeff': coeff, 
            'mean': stats["mean"], 
            'variance': stats["variance"],
            'skewness': stats["skewness"], 
            'kurtosis': stats["kurtosis"], 
            'energy': stats["energy"], 
            'entropy': stats["entropy"], 
            'rms_wavefront': wavefront_metrics["rms_wavefront"], 
            'peak_to_valley': wavefront_metrics["peak_to_valley"], 
            'strehl_ratio': wavefront_metrics["strehl_ratio"], 
            'contrast': texture_metrics["contrast"], 
            'dissimilarity': texture_metrics["dissimilarity"], 
            'homogeneity': texture_metrics["homogeneity"], 
            'energy': texture_metrics["energy"], 
            'peak_signal_noise_ratio': quality_metrics["psnr"], 
            'structural_similarity': quality_metrics['ssim']
        }

    def _save_metadata(self, output_dir: Path):
        """Guarda metadatos técnicos del dataset"""
        metadata = {
            "generation_date": pd.Timestamp.now().isoformat(),
            "optical_parameters": self.config["optical_parameters"],
            "image_height": self.config["metadata"].get("image_height", 512),
            "image_width": self.config["metadata"].get("image_width", 512),
            "noise_profiles": self.config["noise_profiles"],
            "classes": list(self.config["classes"].keys())
        }
        
        with open(output_dir / "metadata.yaml", 'w') as f:
            safe_dump(metadata, f, sort_keys=False)


if __name__ == "__main__": 
    config_path = Path(__file__).parent / "configs" / "pure_aberrations.yaml"
    generator = DatasetGenerator(config_path, print_config=False)

    