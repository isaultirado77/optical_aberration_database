"""
Utilidades para procesamiento de imagenes y manejo de datos
"""

import random
from typing import Union, Tuple, List
import numpy as np
from skimage.io import imsave
import cv2

def normalize_image(image: np.ndarray) -> np.ndarray:
    """ Normaliza una imagen al rango [0, 1]"""
    return (image - image.min()) / (image.max() - image.min())

def save_as_tiff(image: np.ndarray, path: str, normalize: bool = False) -> None: 
    """Guara una imagen en formato TIFF con 16 bits. """
    image_normalized = normalize_image(image)
    image_16bit = (image_normalized * 65535).astype(np.uint16)
    imsave(path, image_16bit)

def add_gaussian_noise(image: np.ndarray,
                       sigma_percent: float = 0.5,
                       clip: bool = True) -> np.ndarray:
    """
    Añade ruido gaussiano a la imagen (simula ruido electrónico del sensor).
    """
    sigma = sigma_percent * np.max(image)
    noise = np.random.normal(0, sigma, image.shape)
    noisy_image = image + noise
    
    if clip:
        return np.clip(noisy_image, image.min(), image.max())
    return noisy_image

def add_poisson_noise(image: np.ndarray,
                      scale: int = 1000,
                      normalize: bool = True) -> np.ndarray:
    """
    Añade ruido Poisson (simula naturaleza cuántica de la luz).
    """
    if normalize:
        image = normalize_image(image)
        
    noisy = np.random.poisson(image * scale) / scale
    
    if normalize:
        return noisy * (image.max() - image.min()) + image.min()
    return noisy


def add_dust_particles(image: np.ndarray,
                       num_particles: Union[int, Tuple[int, int]] = (2, 5),
                       max_radius: int = 15,
                       intensity: float = 0.0) -> np.ndarray:
    """
    Simula partículas de polvo en el sistema óptico (manchas oscuras).
    """
    if isinstance(num_particles, tuple) or isinstance(num_particles, list):
        num_particles = random.randint(*num_particles)
    
    img_height, img_width = image.shape[:2]
    output = image.copy()
    # print("\nWOW", num_particles, isinstance(num_particles, list))
    for _ in range(num_particles):
        x = random.randint(0, img_width - 1)
        y = random.randint(0, img_height - 1)
        radius = random.randint(3, max_radius)
        
        # Dibuja círculos oscuros
        cv2.circle(
            output,
            center=(x, y),
            radius=radius,
            color=intensity,
            thickness=-1  # Relleno
        )
    
    return output


# https://medium.com/@itberrios6/how-to-apply-motion-blur-to-images-75b745e3ef17
def get_random_motion_blur_kernel(ksize: int = 21) -> np.ndarray:
    """Genera un kernel de desenfoque de movimiento aleatorio"""
    center = ksize // 2
    
    options = [
        # 1. Desenfoque circular
        lambda: cv2.circle(np.zeros((ksize, ksize)), 
                          center=(center, center), 
                          radius=center-3, 
                          color=1, 
                          thickness=-1),
        
        # 2. Desenfoque horizontal
        lambda: cv2.line(np.zeros((ksize, ksize)), 
                        pt1=(ksize-1, center), 
                        pt2=(0, center), 
                        color=1, 
                        thickness=1),
        
        # 3. Desenfoque vertical
        lambda: cv2.line(np.zeros((ksize, ksize)), 
                        pt1=(center, ksize - 1), 
                        pt2=(center, 0), 
                        color=1, 
                        thickness=1),
        
        # 4. Desenfoque diagonal
        lambda: cv2.line(np.zeros((ksize, ksize)), 
                        pt1=(0, ksize - 1), 
                        pt2=(ksize - 1, 0), 
                        color=1, 
                        thickness=1),
        
        # 5. Desenfoque direccional personalizado
        lambda: cv2.line(np.zeros((ksize, ksize)),
                        pt1=(center, center),
                        pt2=(center + random.randint(-center+1, center-1),
                             center + random.randint(-center+1, center-1)),
                        color=1,
                        thickness=random.choice([1, 1, 2]))
    ]
    
    kernel = random.choice(options)()
    return kernel / np.sum(kernel) if np.sum(kernel) > 0 else kernel

def add_random_motion_blur(image: np.ndarray, 
                         max_kernel_size: int = 21, 
                         intensity: float = 1.0) -> np.ndarray:
    """
    Aplica desenfoque de movimiento aleatorio a una imagen
    
    Args:
        image: Imagen de entrada
        max_kernel_size: Tamaño máximo del kernel (impar)
        intensity: Intensidad del efecto [0.0-1.0]
    """
    if intensity < 0 or intensity > 1:
        raise ValueError("Intensity must be between 0.0 y 1.0")
    
    ksize = min(max_kernel_size, 25)
    ksize = random.choice([k for k in range(15, 26, 2) if k <= ksize])
    
    kernel = get_random_motion_blur_kernel(ksize)
    
    # Manejo para imágenes en color (3 canales)
    if len(image.shape) == 3:
        blurred = np.stack([cv2.filter2D(image[..., i], -1, kernel) 
                          for i in range(3)], axis = -1)
    else:
        blurred = cv2.filter2D(image, -1, kernel)
    
    return cv2.addWeighted(image, 1 - intensity, blurred, intensity, 0)

