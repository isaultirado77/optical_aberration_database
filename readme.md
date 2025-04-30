# Optical Aberration Database Generator

## Descripción
Sistema para generar datasets sintéticos de aberraciones ópticas simuladas mediante polinomios de Zernike, con capacidad de añadir ruidos físicamente realistas. Características clave:  

- **Simulación física precisa**: Genera interferogramas sintéticos con aberraciones definidas por coeficientes de Zernike.  
- **Control detallado**: Ajuste independiente de modos de aberración clásicos (tilt, defocus, astigmatismo, coma, trefoil, etc.).  
- **Ruidos realistas**: Incorpora modelos físicos de:  
  - Ruido gaussiano (electrónico del sensor)  
  - Ruido Poisson (naturaleza cuántica de la luz)  
  - Partículas de polvo (artefactos ópticos)  
  - Vibración mecánica (desenfoque por movimiento)  

## Instalación
```bash
git clone https://github.com/isaultirado77/optical_aberration_database.git
cd optical_aberration_database
pip install -r requirements.txt
```

## Estructura del Proyecto
```
├── configs/                   # Plantillas YAML de configuración
├── data/                      # Datasets generados
├── src/
│   ├── aberrations/           # Generación de aberraciones
│   ├── metrics/               # Cálculo de métricas
│   └── scripts/               # Scripts para generar y preprocesar datasets
├── tests/                     # Pruebas unitarias
└── docs/                      # Documentación técnica
```

## Uso Básico
### Generar dataset con configuración predeterminada:
```bash
python -m src.scripts.generate_dataset \
    -c configs/pure_aberrations.yaml \
    -o data/my_dataset
```

#### Parámetros vía CLI:
```bash
# Ver todas las opciones
python -m src.scripts.generate_dataset --help

# Ejemplo avanzado
python -m src.scripts.generate_dataset \
    --config custom_config.yaml \
    --output path/to/output \
    --seed 12345
```

#### Configuración YAML
Ejemplo mínimo (`configs/demo.yaml`):
```yaml
metadata:
  simulation_name: "demo_set"
  image_width: 512
  image_height: 512

noise_profiles:
  default_gaussian:
    sigma_percent: 0.5

classes:
  defocus:
    coefficients: [[2, 0, -1.5, 1.5]]
    samples: 100
    noise:
      gaussian: true
```

### Generar datos procesados
Preprocesa imágenes crudas (TIFF) para normalización, aumento de datos y división en conjuntos:

```bash
python -m src.scripts.preprocess_data \
    --input_dir data/generated_pure_aberrations/raw \
    --output_dir data/processed \
    --config configs/preprocess_config.yaml
```

**Parámetros clave**:  
| Argumento      | Descripción                                  | Valor por defecto               |
|----------------|---------------------------------------------|---------------------------------|
| `--input_dir`  | Directorio con imágenes TIFF crudas          | *(Obligatorio)*                 |
| `--output_dir` | Directorio de salida para datos procesados   | *(Obligatorio)*                 |
| `--config`     | Ruta al archivo YAML de configuración       | `configs/preprocess_config.yaml` |

**Estructura de salida**:  
```
output_dir/
├── train/            # 70% de imágenes + aumentos
├── val/              # 15% de imágenes  
└── test/             # 15% de imágenes
```

**Ejemplo de configuración YAML**:  
```yaml
normalize:
  type: "8bit"       # Opciones: "8bit" o "float"

augmentation:
  copies: 2          # Número de aumentos por imagen
  rotation: true     # Rotaciones aleatorias (±15°)
  noise: true        # Añade ruido gaussiano

split:
  test: 0.15         # Proporción para test
  val: 0.15          # Proporción para validación
```

## Métricas Generadas
El dataset incluye automáticamente:

| Categoría          | Métricas Incluidas                     |
|--------------------|----------------------------------------|
| Estadísticas       | Media, varianza, asimetría (skewness), curtosis, energía, entropía|
| Calidad de imagen  | PSNR, SSIM, relación Strehl            |
| Texturas          | Características de Haralick            |
| Zernike           | Coeficientes (n, m) e intensidad por imagen         |

## Documentación Técnica
[Ver documentación detallada](docs/) para:
- Teoría matemática de polinomios de Zernike
- Modelado físico de ruidos ópticos
- Especificación de formatos de archivo

## Contribución
1. Haz fork del proyecto
2. Crea una rama (`git checkout -b feature/nueva-aberracion`)
3. Haz commit de tus cambios (`git commit -m 'Añade soporte para X'`)
4. Haz push a la rama (`git push origin feature/nueva-aberracion`)
5. Abre un Pull Request

## Licencia
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC-BY-NC-SA-4.0)
