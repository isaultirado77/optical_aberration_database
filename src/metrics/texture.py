from typing import Dict
import numpy as np
from skimage.feature import graycomatrix, graycoprops

# https://scikit-image.org/docs/stable/api/skimage.feature.html
# https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.graycoprops
def calculate_haralick_features(image: np.ndarray, distances=[1], angles=[0]) -> Dict[str, float]:
    """
    Calcula 4 características de Haralick a partir de la matriz de co-ocurrencia.
    """
    glcm = graycomatrix(
        (image * 255).astype(np.uint8), 
        distances=distances, 
        angles=angles,
        levels=256,
        symmetric=True
    )
    return {
        'contrast': graycoprops(glcm, 'contrast')[0, 0],
        'dissimilarity': graycoprops(glcm, 'dissimilarity')[0, 0],
        'homogeneity': graycoprops(glcm, 'homogeneity')[0, 0],
        'energy': graycoprops(glcm, 'energy')[0, 0]
    }