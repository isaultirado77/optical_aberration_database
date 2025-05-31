## **Documentación de Configuraciones YAML**

### **1. Configuración para Generación de Datasets (`generate_dataset.py`)**
#### **Estructura Básica**
```yaml
metadata:
  author: "Nombre del Autor"
  simulation_name: "nombre_unico_de_simulación"
  description: "Descripción del dataset"
  image_width: 256    # Ancho en píxeles
  image_height: 256   # Alto en píxeles

optical_parameters:
  wavelength: "632.8nm"  # Longitud de onda simulada

noise_profiles:
  default_gaussian:
    sigma_percent: 0.3   # Intensidad del ruido (0.1-1.0)
    clip: true           # Limitar valores al rango original

classes:
  nombre_clase:
    coefficients: 
      - [n, m, min, max]  # Coeficientes Zernike (n, m) con rango [min, max]
    samples: 50          # Número de muestras
    noise:
      gaussian: true     # Habilitar/deshabilitar ruidos
```

#### **Explicación de Campos**
| Sección            | Campo               | Valores Válidos       | Descripción                                  |
|--------------------|---------------------|-----------------------|----------------------------------------------|
| `metadata`         | `simulation_name`   | String único          | Identificador del dataset generado           |
| `optical_parameters` | `wavelength`       | Ej: "532nm", "1064nm" | Longitud de onda para cálculos físicos       |
| `noise_profiles`   | `default_gaussian`  | `sigma_percent: 0.0-1.0` | Ruido electrónico del sensor               |
|                    | `default_poisson`   | `scale: 100-10000`    | Ruido cuántico de la luz (fotones)          |
|                    | `default_dust`      | `num_particles: int`  | Partículas de polvo (manchas oscuras)       |
|                    | `default_vibration` | `max_kernel_size: odd_int` | Desenfoque por vibración mecánica       |
| `classes`          | `coefficients`      | Lista de [n, m, min, max] | Combinaciones de modos Zernike y sus rangos |

---

- Para consultar [información](docs/noise_models.md) respecto a la configuración de ruidos consultar `docs/noise_models.md`. 

### **2. Configuración para Preprocesamiento (`preprocess_data.py`)**
#### **Estructura Básica**
```yaml
#configs/preprocess_config.yaml

seed: 42                       # Semilla para reproducibilidad

normalize:
  type: "8bit"                 # "8bit" o "float"

augmentation:
  copies: 2                    # Número de aumentos por imagen
  rotation: True               # Aplicar rotaciones aleatorias
  noise: True                  # Añadir ruido gaussiano

split:
  test: 0.15                   # 15% para test
  val: 0.15                    # 15% para validación
  # El 70% restante es para entrenamiento
```

#### **Explicación de Campos Clave**
| Sección          | Campo         | Valores Válidos    | Descripción                                  |
|------------------|---------------|--------------------|----------------------------------------------|
| `normalize`      | `type`        | "8bit" o "float"   | Tipo de normalización de píxeles            |
| `augmentation`   | `copies`      | Entero ≥1          | Número de imágenes aumentadas por original  |
| `split`          | `test`/`val`  | 0.0-1.0            | Proporciones para división del dataset      |

---

### **3. Archivo `demo.yaml` (Ejemplo Integrado)**
```yaml
metadata:
  simulation_name: "demo_aberrations"
  image_width: 512
  image_height: 512

optical_parameters:
  wavelength: "532nm"

noise_profiles:
  default_gaussian:
    sigma_percent: 0.4
    clip: false  # Permite valores fuera de rango

classes:
  simple_defocus:
    coefficients:
      - [2, 0, -2.0, 2.0]  # Defocus fuerte
    samples: 30
    noise:
      gaussian: true
      dust: 
        num_particles: [3, 5]

  coma_spherical:
    coefficients:
      - [3, 1, -0.7, 0.7]    # Coma horizontal
      - [4, 0, -0.4, 0.4]     # Esférica
    samples: 30
    noise:
      vibration:
        max_kernel_size: 25
      gaussian: true
      poisson: true
      dust: true
```

---

### **Cómo Usar los Archivos de Configuración**
1. **Generación de Datos**:
```bash  
python -m src.scripts.generate_dataset \  
  -c configs/demo.yaml \  
  -o data/demo_output
```  

2. **Preprocesamiento**:
  ```bash  
python -m src.scripts.preprocess_data \  
    -i data/demo_output/raw \  
    -o data/demo_output/processed \  
    --config configs/preprocess.yaml  
```  

---

### **Notas Clave**
- **Reproducibilidad**: Usar siempre `seed` para resultados consistentes.
- **Seguridad de Tipos**: Los coeficientes Zernike deben ser enteros (n, m).
- **Rendimiento**: Para imágenes >1024x1024, aumentar `sigma_percent` proporcionalmente.

---

### **Plantilla para Nuevas Aberraciones**
```yaml
custom_aberration:
  coefficients:
    - [5, 3, -0.7, 0.7]  # Pentafoil
    - [6, 0, -0.3, 0.3]   # Aberración de 6to orden
  samples: 100
  noise:
    poisson: 
      scale: 500  # Ajustar para ruido cuántico
```