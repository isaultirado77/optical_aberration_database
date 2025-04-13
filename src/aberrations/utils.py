"""
Utilidades para procesamiento de imagenes y manejo de datos
"""

import numpy as np
from skimage.io import imsave
# from skimage import img_as_ubyte


def normalize_image(image: np.ndarray) -> np.ndarray:
    """ Normaliza una imagen al rango [0, 1]"""
    return (image - image.min()) / (image.max() - image.min())

def save_as_fiff(image: np.ndarray, path: str) -> None: 
    """Guara una imagen en formato TIFF con 16 bits. """
    image_normalized = normalize_image(image)
    image_16bit = (image_normalized * 65535).astype(np.uint16)
    imsave(path, image_16bit)

def gaussian_noise(): 
    pass

