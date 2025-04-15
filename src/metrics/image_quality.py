import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from typing import Dict, Tuple

import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

def calculate_psnr(reference: np.ndarray, distorted: np.ndarray) -> float:
    """
    Calcula el Peak Signal-to-Noise Ratio (PSNR).
    
    Args:
        reference: Imagen de referencia (sin aberraciones).
        distorted: Imagen distorsionada.
    
    Returns:
        Valor de PSNR en decibeles.
    """
    return peak_signal_noise_ratio(reference, distorted, data_range=1.0)

def calculate_ssim(reference: np.ndarray, distorted: np.ndarray) -> float:
    """
    Calcula el Structural Similarity Index (SSIM).
    """
    return structural_similarity(
        reference, distorted, 
        win_size=11, gaussian_weights=True, 
        data_range=1.0, channel_axis=None
    )

def calculate_image_quality_metrics(reference: np.ndarray, distorted: np.ndarray) -> Dict[str, float]: 
    return {
        "psnr": calculate_psnr(reference, distorted),
        "ssim": calculate_psnr(reference, distorted)
    }