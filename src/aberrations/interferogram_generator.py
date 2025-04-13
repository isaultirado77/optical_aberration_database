"""
Generación de interferogramas sintéticos a partir de frentes de onda aberrados. 
"""

import numpy as np
from .zernike_polynomials import generate_wavefront
from .utils import normalize_image
from typing import Dict, Tuple


def generate_interferogram(coefficients: Dict[Tuple[int, int], float],
                           shape: Tuple[int, int] = (512, 512)) -> np.ndarray:
    """
    Genera un intergerograma sintético con aberraciones definidas
    """
    wavefront = generate_wavefront(coefficients, shape)
    interferogram = np.cos(2 * np.pi * wavefront)
    return normalize_image(interferogram)
