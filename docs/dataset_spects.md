# **Documentación de los Datasets Generados**  
*(Estructura y contenido generado por `generate_dataset.py` y `preprocess_data.py`)*  


## **Descripción General**  

Los datasets generados por este sistema son **colecciones interferogramas de sintéticos** que simulan aberraciones ópticas en condiciones de laboratorio controladas. Cada dataset incluye:  

- **Imágenes crudas**: Interferogramas en formato TIFF 16-bit (256x256px a 1024x1024px).  
- **Metadatos técnicos**: Configuración exacta de aberraciones y ruidos aplicados.  
- **Métricas cuantitativas**: 20+ indicadores de calidad óptica y estadísticos.  

---

## 1. Datasets Generados por `generate_dataset.py`  
Este script produce datasets sintéticos de **interferogramas con aberraciones ópticas** y ruidos simulados.  

### **Estructura de Salida**  
```
nombre_dataset/  
├── raw/                          # Interferogramas crudos en TIFF  
│   ├── defocus_0001.tiff         # Formato: <clase>_<id>.tiff  
│   ├── astigmatism_0002.tiff  
│   └── ...  
├── dataset_metadata.yaml         # Configuración exacta usada  
└── dataset_metrics.csv           # Métricas ópticas y estadísticas  
```

### **Contenido Generado**  
| Componente               | Descripción |  
|--------------------------|-------------|  
| **Imágenes TIFF (raw/)** | Interferogramas en 16-bit (0-65535) con aberraciones aplicadas. |  
| **metadata.yaml**        | Copia de la configuración YAML usada, incluyendo: <br> - Parámetros ópticos (λ, resolución) <br> - Coeficientes Zernike por clase <br> - Perfiles de ruido aplicados. |  
| **metrics.csv**          | Datos cuantitativos por imagen: <br> - Modos Zernike (n, m, coeff) <br> - RMS, Strehl, PSNR, SSIM <br> - Estadísticas (media, entropía, etc.). |  

---

## **2. Datasets Preprocesados por `preprocess_data.py`**  
Transforma los datos crudos en datasets listos para Machine Learning.  

### **Estructura de Salida**  
```
processed_dataset/  
├── train/                      # 70% de los datos  
│   ├── image_0001.tiff         # Imágenes aumentadas  
│   ├── image_0001_aug0.tiff    # Versión rotada  
│   └── ...  
├── val/                        # 15% de los datos  
│   └── ...  
└── test/                       # 15% de los datos (sin aumentos)  
    └── ...  
```

### **Procesamiento Aplicado**  
| Paso               | Descripción |  
|--------------------|-------------|  
| **Normalización**  | Convierte a 8-bit (0-255) o float (0-1). |  
| **Aumento**       | Genera copias con: <br> - Rotaciones ($\pm15°$) <br> - Ruido gaussiano ($\sigma=0.05$) <br> - Volteos horizontales (opcional). |  
| **División**      | Separa en train/val/test según proporciones definidas. 

- **Nota**: En la tabla anterior se ha considerado el uso del archivo de configuración en `configs/preprocess_config.yaml`. 

---

## **3. Ejemplo de Pipeline Completo**  

### **Paso 1: Generación del Dataset**  
```bash  
python -m src.scripts.generate_dataset \  
    -c configs/demo.yaml \  
    -o data/demo_output
```  
**Genera**:  
- `data/demo_output/raw/*.tiff` (imágenes)  
- `data/demo_output/metrics.csv` (métricas)  
- `data/demo_output/metadata.yaml` (metadata)

### **Paso 2: Preprocesamiento**  
```bash  
python -m src.scripts.preprocess_data \  
    -i data/demo_output/raw \  
    -o data/demo_output/processed \  
    --config configs/preprocess.yaml  
```  
**Resultado**:  
- Directorio `data/demo_output/processed/` con subcarpetas `train/`, `val/`, `test/`.  

---

## **4. Notas Clave**  
1. **Reproducibilidad**:  
   - Los YAML guardados (`metadata.yaml`) permiten regenerar datasets idénticos.  
2. **Compatibilidad**:  
   - Las imágenes TIFF son compatibles con:  
     - OpenCV, scikit-image, TensorFlow, PyTorch.  
3. **Personalización**:  
   - Modifica los archivos YAML para ajustar:  
     - Tipos de aberraciones (`classes:`).  
     - Intensidad de ruidos (`noise_profiles:`).  

--- 
