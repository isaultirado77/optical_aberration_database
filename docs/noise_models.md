# Modelos de Ruido Implementados

## 1. Ruido Gaussiano  
**Archivo**: `utils.py` → `add_gaussian_noise()`  
**Física**: Simula ruido electrónico en sensores.  
**Parámetros YAML**:  
```yaml
noise_profiles:
  default_gaussian:
    sigma_percent: 0.3  # % del valor máximo de la imagen
    clip: true          # Recorta valores al rango original
```

## 2. Ruido Poisson  
**Archivo**: `utils.py` → `add_poisson_noise()`  
**Física**: Modela la naturaleza cuántica de la luz.  
**Parámetros YAML**:  
```yaml
  default_poisson:
    scale: 1000         # Intensidad del efecto (mayor = menos ruido)
    normalize: true     # Mantiene el rango [0, 1]
```

## 3. Partículas de Polvo  
**Archivo**: `utils.py` → `add_dust_particles()`  
**Física**: Simula suciedad en componentes ópticos.  
**Parámetros YAML**:  
```yaml
  default_dust:
    num_particles: [3, 5]  # Rango aleatorio de partículas
    max_radius: 15         # Radio máximo en píxeles
    intensity: 0.0         # 0=negro, 1=blanco
```

## 4. Vibración Mecánica  
**Archivo**: `utils.py` → `add_random_motion_blur()`  
**Física**: Desenfoque por movimiento en sistemas no estables.  
**Parámetros YAML**:  
```yaml
  default_vibration:
    max_kernel_size: 21    # Tamaño del kernel (impar)
    intensity: 0.8         # 0=sin efecto, 1=completo
```

---

### **3. Ejemplo de Configuración Completa**  
```yaml
noise_profiles:
  default_gaussian:
    sigma_percent: 0.4
    clip: false

  default_poisson:
    scale: 500
    normalize: true

  default_dust:
    num_particles: [5, 10]
    max_radius: 20

  default_vibration:
    max_kernel_size: 15
    intensity: 0.5

classes:
  high_noise_spherical:
    coefficients: 
    - [4, 0, -0.4, 0.4] 
    samples: 50
    noise:
      gaussian: true
      poisson: true
      dust: true
      vibration: true
```

#### **Fundamentación de la Estructura de Ruidos**  

La arquitectura de ruidos implementada (*Gaussiano*, *Poisson*, *Polvo* y *Vibración*) replica **condiciones realistas de laboratorios ópticos**, donde estos efectos emergen de:  

1. **Ruido Gaussiano**  
   - *Origen*: Electrónica del sensor.  
   - *Contexto experimental*: Dominante en experimentos con baja iluminación.  

2. **Ruido Poisson**  
   - *Origen*: Naturaleza cuántica de la luz.  
   - *Contexto experimental*: En sistemas láser de baja potencia o imágenes de fluorescencia.  

3. **Partículas de Polvo**  
   - *Origen*: Contaminación en lentes/espejos o medio ambiente.  
   - *Contexto experimental*: Típico en sistemas sin purgas de aire o montajes no herméticos.  

4. **Vibración Mecánica**  
   - *Origen*: Movimientos en mesas ópticas no aisladas o equipos adjuntos (ventiladores, bombas).  
   - *Contexto experimental*: Común en interferometría de alta precisión o microscopía.  

**Diseño de la Implementación**:  
Los parámetros en los YAML permiten ajustar **magnitudes físicas reales** (ej: `sigma_percent` para el ruido electrónico o `num_particles` para densidad de polvo), facilitando la simulación de escenarios específicos (*ej: un laboratorio con alto tráfico de personas = mayor vibración*).  

---

### **Recomendaciones de Uso**  
1. **Jerarquía de Configuración**:  
   - Los parámetros en `classes.[nombre].noise` activan/desactivan ruidos.  
   - Los valores detallados se definen en `noise_profiles.default_*`.  

2. **Debugging**:  
   ```python
   # Para verificar ruidos aplicados
   from src.aberrations.utils import add_gaussian_noise, add_dust_particles
   debug_img = add_dust_particles(clean_img, num_particles=5)
   ```

3. **Customización**:  
   Extender los modelos en `src/aberrations/utils.py` siguiendo el patrón:  
   ```python
   def add_custom_noise(image, **params):
       # Implementar nuevo modelo aquí
       return noisy_image
   ```
