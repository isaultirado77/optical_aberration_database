"""
Herramientas de visualización para aberraciones ópticas. 
Genera ejemplos de gráficos de frentes de onda e interferogramas para documentación.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, Tuple
from src.aberrations import generate_interferogram

Path("visualization/plots").mkdir(parents=True, exist_ok=True)

def plot_wavefront(wavefront: np.ndarray, 
                   title: str = "Aberrated wavefront", 
                   cmap: str = "viridis", 
                   show_colorbar: bool = True, 
                   save: bool = False,
                   filename: str = "wavefront.png") -> None:
    plt.figure(figsize=(8, 6))
    img = plt.imshow(wavefront, cmap=cmap)
    plt.title(title)
    if show_colorbar:
        plt.colorbar(img, label="Amplitude (λ)")
    plt.axis("off")
    
    if save:
        plt.savefig(f"visualization/plots/{filename}", 
                   bbox_inches='tight', 
                   dpi=150,
                   transparent=True)
    plt.close()

def main():
    # Pure defocus
    defocus = generate_interferogram({(2,0): 1.5})
    plot_wavefront(defocus, 
                  title="Pure Defocus (Z₂⁰)", 
                  save=True,
                  filename="defocus_wavefront.png")
    
    # Coma + astigmatism
    coma_astig = generate_interferogram({
        (3,1): 0.8,  # Coma
        (2,-2): -0.5  # Astigmatism
    })
    plot_wavefront(coma_astig,
                  title="Coma (Z₃¹) + Astigmatism (Z₂⁻²)",
                  save=True,
                  filename="coma_astigmatism_wavefront.png")
    
    # High-order aberration
    high_order = generate_interferogram({
        (4,0): 0.6,   # Spherical
        (3,3): -0.4,   # Trefoil
        (1,-1): 1.2    # Tilt
    })
    plot_wavefront(high_order,
                  title="High-Order Aberrations",
                  save=True,
                  filename="high_order_wavefront.png")
    

if __name__ == '__main__':
    main()