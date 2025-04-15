"""
Modulo para cálculo de métricas de imagenes con aberraciones ópticas.

Bibliografia: 
 - http://www.iste.co.uk/data/doc_noyoaiyjtdiw.pdf
 - https://www.scirp.org/journal/paperinformation?paperid=90911
 - https://scikit-image.org/docs/0.25.x/api/skimage.metrics.html
 - https://scikit-image.org/docs/stable/api/skimage.feature.html
 - https://github.com/thathegdegirl/haralick-textural-feature-analysis-1/blob/master/original%20paper.pdf
 - https://en.wikipedia.org/wiki/Co-occurrence_matrix
"""

from .statistical import calculate_statistics
from .image_quality import calculate_psnr, calculate_ssim
from .texture import calculate_haralick_features
from .zernike_metrics import calculate_wavefront_error

__all__ = [
    'calculate_statistics',
    'calculate_psnr',
    'calculate_ssim',
    'calculate_haralick_features',
    'calculate_wavefront_error'
]