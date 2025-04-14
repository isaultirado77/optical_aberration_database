import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
from tqdm import tqdm
from ..aberrations.interferogram_generator import generate_interferogram
from ..aberrations.utils import add_gaussian_noise, add_poisson_noise, add_dust_particles, add_random_motion_blur, save_as_tiff
 # from ..metrics import image_quality, statistical, texture, zernike_metrics

@dataclass
class AberrationConfig: 
    pass

class DatasetGenerator: 
    pass

if __name__ == "__main__": 
    pass
