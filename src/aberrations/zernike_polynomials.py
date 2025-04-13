"""
"""

import numpy as np
import matplotlib.pyplot as plt
from math import factorial
from typing import Dict, Tuple, Optional

# https://en.wikipedia.org/wiki/Zernike_polynomials
def zernike_radial_coeff(n: int, m: int, k: int) -> float:
    """
    """
    sign = (-1)**k 
    numerator = factorial(n - k)
    denominator = (factorial(k) * 
                  factorial((n + abs(m)) // 2 - k) * 
                  factorial((n - abs(m)) // 2 - k))
    return sign * numerator / denominator

def zernike_radial(n: int, m: int, rho: np.ndarray) -> np.ndarray:
    """
    """
    R = np.zeros_like(rho)
    for k in range((n - abs(m)) // 2 + 1):
        R += zernike_radial_coeff(n, m, k) * rho**(n - 2 * k)
    return R

def zernike_polynomial(n: int, m: int, rho: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """
    """
    if m > 0: 
        return zernike_radial(n, m, rho) * np.cos(m * theta)
    elif m < 0: 
        return zernike_radial(n, -m, rho) * np.sin(-m * theta)
    else:
        return zernike_radial(n, 0, rho)

def generate_wavefront(coefficients: Dict[Tuple[int, int], float], 
                       shape: Tuple[int, int] = (512, 512), 
                       mask_circle: bool = True) -> np.ndarray:
    """
    """
    # Generar coordenadas normalizadas
    x = np.linspace(-1, 1, shape[0])
    y = np.linspace(-1, 1, shape[1])
    xx, yy = np.meshgrid(x, y)
    rho = np.sqrt(xx**2 + yy**2)
    theta = np.arctan2(yy, xx)

    # Inivializar frente de onda
    wavefront = np.zeros(shape)
    for (n, m), coeff in coefficients.items(): 
        wavefront += coeff * zernike_polynomial(n, m, rho, theta)

    # Aplicar mask circular
    if mask_circle: 
        wavefront[rho > 1] = 0

    return wavefront

def plot_wavefront(wavefront: np.ndarray, 
                   title: str = "Aberrated wavefront", 
                   cmap: str = "jet", 
                   show_colorbar: bool = True) -> None:
    """
    """

    plt.figure(figsize=(8, 6))
    plt.imshow(wavefront, cmap=cmap)
    plt.title(title)
    if show_colorbar: 
        plt.colorbar(label="Amplitude")
    plt.axis("off")
    plt.show()


if __name__ == "__main__": 
    # Coefficientes para aberraci+on de coma(Z_3^1) y astigmatismo (Z_2^{-2})
    coefficients = {
        (3, 1): 0.8,  # Coma
        (2, -2): -0.5  # Astigmatism
        }
    # Generar y visualizar frente de onda
    wavefront = generate_wavefront(coefficients)
    plot_wavefront(wavefront, title=r"Coma + Astigmatism (Z[3,1] + Z[2, -2])")