# **Implementación de Polinomios de Zernike**  
---

## **Introducción**  
Este documento complementa [`optical_aberrations.md`](./optical_aberrations.md) — donde se explica la relación entre los polinomios de Zernike y las aberraciones ópticas— detallando **la implementación concreta en el código** (módulo `src/aberrations/`).  

Los scripts principales son:  
1. **`zernike_polynomials.py`**: Cálculo de modos Zernike y generación de frentes de onda.  
2. **`interferogram_generator.py`**: Transformación del frente de onda a interferogramas sintéticos.  

---

## **Módulo `zernike_polynomials.py`**  

### **1. Componentes Matemáticos**  
#### **`zernike_radial_coeff(n, m, k)`**  
Calcula los coeficientes del polinomio radial $R_n^m(\rho)$:  
```python  
def zernike_radial_coeff(n: int, m: int, k: int) -> float:  
    sign = (-1)**k  
    numerator = factorial(n - k)  
    denominator = (factorial(k) *  
                  factorial((n + abs(m)) // 2 - k) *  
                  factorial((n - abs(m)) // 2 - k))  
    return sign * numerator / denominator  
```  
**Fórmula asociada**:  
$$ R_n^m(\rho) = \sum_{k=0}^{(n-|m|)/2} \frac{(-1)^k (n-k)!}{k! \left(\frac{n+|m|}{2} - k\right)! \left(\frac{n-|m|}{2} - k\right)!} \rho^{n-2k} $$  

---

#### **`zernike_polynomial(n, m, rho, theta)`**  
Combina componentes radiales y angulares para obtener el modo completo:  
```python  
def zernike_polynomial(n: int, m: int, rho: np.ndarray, theta: np.ndarray) -> np.ndarray:  
    if m > 0:  
        return zernike_radial(n, m, rho) * np.cos(m * theta)  # Modos coseno  
    elif m < 0:  
        return zernike_radial(n, -m, rho) * np.sin(-m * theta)  # Modos seno  
    else:  
        return zernike_radial(n, 0, rho)  # Modos sin dependencia angular  
```  

---

### **2. Generación de Frentes de Onda**  
#### **`generate_wavefront(coefficients, shape, mask_circle)`**  
Combina múltiples modos Zernike para crear un frente de onda aberrado:  
```python  
def generate_wavefront(coefficients: Dict[Tuple[int, int], float],  
                       shape: Tuple[int, int] = (512, 512),  
                       mask_circle: bool = True) -> np.ndarray:  
    # 1. Generar coordenadas normalizadas  
    x = np.linspace(-1, 1, shape[0])  
    y = np.linspace(-1, 1, shape[1])  
    xx, yy = np.meshgrid(x, y)  
    rho = np.sqrt(xx**2 + yy**2)  
    theta = np.arctan2(yy, xx)  

    # 2. Sumar contribuciones de cada modo  
    wavefront = np.zeros(shape)  
    for (n, m), coeff in coefficients.items():  
        wavefront += coeff * zernike_polynomial(n, m, rho, theta)  

    # 3. Aplicar máscara circular (opcional)  
    if mask_circle:  
        wavefront[rho > 1] = 0  

    return wavefront  
```  

---

## **Módulo `interferogram_generator.py`**  
#### **`generate_interferogram(coefficients, shape)`**  
Convierte el frente de onda en un **interferograma sintético** que simula el patrón de interferencia de un interferómetro real:  

```python
def generate_interferogram(coefficients: Dict[Tuple[int, int], float],
                           shape: Tuple[int, int] = (512, 512)) -> np.ndarray:
    wavefront = generate_wavefront(coefficients, shape)
    interferogram = np.cos(2 * np.pi * wavefront)  # Transformación clave
    return normalize_image(interferogram)
```

### **Física del Interferograma**  
La ecuación:  
$$ I(\rho, \theta) = \cos(2\pi \cdot W(\rho, \theta)) $$  

- **$I(\rho, \theta)$**: Intensidad del interferograma en coordenadas normalizadas.  
  - *Rango*: `[-1, 1]` antes de normalización.  
- **$W(\rho, \theta)$**: Frente de onda aberrado (en unidades de longitud de onda, λ).  
  - Calculado como la suma ponderada de modos Zernike.  

#### **Base Física**:  
1. **Principio de Interferencia**:  
   - El interferograma simula la interferencia entre un frente de onda de referencia (plano) y el frente aberrado.  
   - Los máximos/mínimos de intensidad corresponden a diferencias de fase constructiva/destructiva.  

2. **Interpretación de los Patrones**:  
   - **Franjas rectas**: Sin aberraciones ($W=0$).  
   - **Distorsiones en franjas**: Aberraciones ópticas ($W \neq 0$).  

3. **Normalización**:  
   - `normalize_image()` escala los valores a `[0, 1]` para representación (equivalente a ajustar el contraste en un interferómetro real).  

---


## **Visualización**  
#### **`plot_wavefront(wavefront, title, cmap)`**  
Muestra el frente de onda aberrado:  
```python  
def plot_wavefront(wavefront: np.ndarray,  
                   title: str = "Aberrated wavefront",  
                   cmap: str = "viridis") -> None:  
    plt.imshow(wavefront, cmap=cmap)  
    plt.colorbar(label="Amplitude (λ)")  
    plt.title(title)  
    plt.axis("off")  
    plt.show()  
```  
**Ejemplo de uso**:  
```python  
coefficients = {(3, 1): 0.8, (2, -2): -0.5}  # Coma + Astigmatismo  
wavefront = generate_wavefront(coefficients)  
plot_wavefront(wavefront, title="Coma + Astigmatismo")  
```  

---
### **Ejemplos Visuales**

#### 1. Aberración Pura (Defocus)
![Defocus Z₂⁰](/visualization/plots/defocus_wavefront.png){: width="300" height="300"}  
**Coeficientes**: `{(2,0): 1.5}`  
- Modo esférico simétrico típico en sistemas desenfocados.

#### 2. Aberración Mixta (Coma + Astigmatismo)
![Coma + Astigmatismo](/visualization/plots/coma_astigmatism_wavefront.png){: width="300" height="300"}  
**Coeficientes**: `{(3,1): 0.8, (2,-2): -0.5}`  
- Distorsión asimétrica (coma) combinada con elongación axial (astigmatismo).

#### 3. Aberraciones de Alto Orden
![Alto Orden](/visualization/plots/high_order_wavefront.png){: width="300" height="300"}- Combinación de aberración esférica, trefoil y tilt.


---

## Convenciones  
1. **Coordenadas**:  
   - $\rho \in [0, 1]$: Radio normalizado.  
   - $\theta \in [-\pi, \pi]$: Ángulo azimutal.  

2. **Coeficientes**:  
   - En unidades de longitud de onda (λ).  
   - Positivos: Aberración "sobrecorregida".  

3. **Límites**:  
   - Órdenes implementados: $n \leq 4$ (14 modos).  