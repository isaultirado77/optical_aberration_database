import numpy as np
from typing import Dict



def calculate_mean(image: np.ndarray) -> float:
    """Calcula la media de los valores de píxel"""
    return float(np.mean(image))

def calculate_variance(image: np.ndarray) -> float:
    """Calcula la varianza de los valores de píxel"""
    return float(np.var(image))

# Skewness & Kurtosis: https://stats.libretexts.org/Bookshelves/Probability_Theory/Probability_Mathematical_Statistics_and_Stochastic_Processes_(Siegrist)/04%3A_Expected_Value/4.04%3A_Skewness_and_Kurtosis
def calculate_skewness(image: np.ndarray) -> float:
    """Calcula la asimetría estadística (skewness)"""
    flat_img = image.flatten()
    mean = np.mean(flat_img)
    median = np.median(flat_img)
    std = np.std(flat_img)
    return float(3 * (mean - median) / std) if std != 0 else 0.0

def calculate_kurtosis(image: np.ndarray) -> float:
    """Calcula la curtosis (grado de 'picudez')"""
    flat_img = image.flatten()
    mean = np.mean(flat_img)
    var = np.var(flat_img)
    if var == 0:
        return 0.0
    return float(np.mean((flat_img - mean)**4) / var**2)

# Energy: https://stackoverflow.com/questions/4562801/what-is-energy-in-image-processing
def calculate_energy(image: np.ndarray) -> float:
    """Calcula la energía de la imagen (suma de cuadrados)"""
    return float(np.sum(image**2))

# Entropy: https://stackoverflow.com/questions/50313114/what-is-the-entropy-of-an-image-and-how-is-it-calculated
def calculate_entropy(image: np.ndarray, bins: int = 256) -> float:
    """Calcula la entropía de la imagen"""
    hist, _ = np.histogram(image, bins=bins, range=(0, 1))
    hist = hist[hist > 0] / image.size  # Normaliza y elimina ceros
    return float(-np.sum(hist * np.log2(hist)))

def calculate_statistics(image: np.ndarray) -> Dict[str, float]:
    """
    Calcula momentos estadísticos básicos de una imagen.
    
    Args:
        image: Array 2D de la imagen (puede ser el interferograma o frente de onda).
    
    Returns:
        Diccionario con métricas clave.
    """
    return {
        'mean': calculate_mean(image),
        'variance': calculate_variance(image),
        'skewness': calculate_skewness(image),
        'kurtosis': calculate_kurtosis(image),
        'energy': calculate_energy(image),
        'entropy': calculate_entropy(image)
    }
