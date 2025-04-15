from yaml import safe_load
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
from tqdm import tqdm
"""from aberrations import (
    generate_interferogram, 
    add_gaussian_noise, 
    add_poisson_noise, 
    add_dust_particles, 
    add_random_motion_blur, 
    save_as_tiff
)
from metrics import (
    calculate_statistics, 
    calculate_psnr, 
    calculate_ssim, 
    calculate_haralick_features, 
    calculate_wavefront_error
)"""


@dataclass
class AberrationConfig:
    name = str
    coefficients: List[Tuple[int, int, float, float]]  # (n, m, min, max)
    samples: int
    noise: Dict[str, bool]

class DatasetGenerator: 
    def __init__(self, config_path: Path, print_config: bool = False):
        print("INIT GENERATOR")
        self.config = self._load_config(config_path)
        self.rng = np.random.default_rng(self.config['metadata'].get("seed", 42))  # Generador de números aleatorios con semilla fija (para reproducibilidad).
        if print_config: 
            self._print_config()

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
    
    def _generate_coefficients(self, aberration: dict) -> Dict[Tuple[int, int], float]: 
        pass

    def _apply_noises(self, image: np.ndarray, noise_config: Dict[str, bool]) -> np.ndarray: 
        pass

    def _generate_dataset(self, output_dir: Path) -> None: 
        pass

if __name__ == "__main__": 
    config_path = Path("configs/pure_aberrations.yaml")
    generator = DatasetGenerator(config_path, print_config=True)
