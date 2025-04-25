from pathlib import Path
from typing import List
import argparse
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import yaml

class DataPreprocessor: 
    def __init__(self, config_path: Path, input_dir: Path, output_dir: Path):
        self.config = self._load_config(config_path)
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.rng = np.random.default_rng(self.config["seed"])


    def _load_config(self, path: Path) -> dict:
        with open(path) as f: 
            return yaml.safe_load(f)

    def normalize_image(self, image: np.ndarray) -> np.ndarray:
        """Convierte imagenes 8-bit (0-255) o normaliza a [0, 1]."""
        if self.config["normalize"]["type"] == "8bit": 
            return ((image - image.min()) * (255 / (image.max() - image.min()))).astype(np.uint8)
        
        elif self.config["normalize"]["type"] == "float":
            return (image - image.min()) / (image.max() -image.min()) 
        
    def augment_image(self, image: np.ndarray) -> List[np.ndarray]: 
        """Genera versiones aumentadas de una imagen. """
        augmented = []

        for _ in range(self.config["augmentation"]["copies"]): 
            # Rotación
            if self.config["augmentation"]["rotation"]: 
                angle = self.rng.uniform(-15, 15)
                M = cv2.getRotationMatrix2D((image.shape[1]/2, image.shape[0]/2), angle, 1)
                rotated = cv2.warpAffine(image, M, image.shape[::-1])
                augmented.append(rotated)


            # Ruido gaussiano
            if self.config["augmentation"]["noise"]: 
                noise = self.rng.normal(0, 0.05, image.shape)
                noisy = np.clip(image + noise, 0, 1)
                augmented.append(noisy)
        return augmented

    def split_dataset(self, filepaths: List[Path]) -> dict:
        """Divide las rutas de archivos en train/val/test."""
        train, test = train_test_split(
            filepaths, 
            test_size=self.config["split"]["test"],
            random_state=self.config["seed"]
        )
        train, val = train_test_split(
            train, 
            test_size=self.config["split"]["val"],
            random_state=self.config["seed"]
        )
        return {"train": train, "val": val, "test": test}

    def run(self): 
        # 1. Cargar tutas de imagenes originales
        images = list(self.input_dir.glob("*.tiff"))

        # 2. Dividir dataset
        splits = self.split_dataset(images)

        # 3. Procesar cada grupo
        for split_name, files in splits.items(): 
            split_output_dir = self.output_dir / split_name
            split_output_dir.mkdir(parents=True, exist_ok=True)


            for file in tqdm(files, desc=f"Processing {split_name}"): 
                image = cv2.imread(str(file), cv2.IMREAD_UNCHANGED)
                image_norm = self.normalize_image(image)

                # Guardar imagen base
                cv2.imwrite(str(split_output_dir / file.name), image_norm)

                # Generar aumentos si es train
                if split_name == "train":
                    for i, aug in enumerate(self.augment_image(image_norm)):
                        cv2.imwrite(str(split_output_dir / f"{file.stem}_aug{i}.tiff"), aug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preprocesamiento de imágenes según el archivo de configuración YAML.')
    parser.add_argument(
        '--config',
        type=Path,
        default=Path(__file__).parent.parent.parent / "configs" / "preprocess_config.yaml",
        help='Ruta al archivo de configuración YAML (por defecto: configs/preprocess_config.yaml).'
    )
    parser.add_argument(
        '-i', '--input_dir',
        type=Path,
        required=True,
        help='Ruta al directorio de imágenes TIFF de entrada.'
    )
    parser.add_argument(
        '-o', '--output_dir',
        type=Path,
        required=True,
        help='Ruta al directorio de salida para guardar imágenes procesadas.'
    )

    args = parser.parse_args()
    preprocessor = DataPreprocessor(args.config, args.input_dir, args.output_dir)
    preprocessor.run()

