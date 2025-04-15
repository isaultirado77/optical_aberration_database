# https://www.telescope-optics.net/aberrations.htm#pattern
# https://www.telescope-optics.net/Strehl.htm

import numpy as np
from typing import Dict

def calculate_wavefront_error(wavefront: np.ndarray) -> Dict[str, float]:
    """
    Calcula métricas físicas del frente de onda aberrado.
    """
    rms = np.sqrt(np.mean(wavefront**2))
    ptv = np.max(wavefront) - np.min(wavefront)
    return {
        'rms_wavefront': float(rms),  #rms: root mean squared error
        'peak_to_valley': float(ptv),
        'strehl_ratio': float(np.exp(-(2 * np.pi * rms)**2))  # Aproximación
    }