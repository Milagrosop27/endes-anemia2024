Análisis de la Asociación entre el Índice de Bienestar del Hogar y la Anemia en Niños Menores de 5 Años en Perú (ENDES 2024)
---
---
#### Nota: Muchas gracias por revisar mi proyecto. Y por las maravillosas clases brindadas, que me han permitido desarrollar este análisis. Espero sugerencia o comentarios ya sean constructivos o de cualquier tipo. Aún faltan algunos detalles por desarrollar, pero espero que el avance actual sea de su agrado. Asimismo, si lo puedo subir a GitHub, Linkedin y etiquetarlo :D

---
## 1. Descripción General
Este proyecto investiga la relación entre el índice de bienestar socioeconómico del hogar y la severidad de la anemia en niños de 6 a 59 meses en Perú, utilizando datos de la Encuesta Demográfica y de Salud Familiar (ENDES) 2024. Se ajusta un modelo de regresión ordinal logit para determinar si los hogares con menor bienestar (medido a través de un índice de riqueza categorizado en quintiles) presentan una mayor probabilidad de tener niños con anemia más grave.
## 2. Hipótesis
- **Hipótesis Nula (H0)**: El índice de bienestar del hogar no se asocia con la presencia ni la gravedad de la anemia en niños de 6-59 meses.
- **Hipótesis Alternativa (H1)**: El índice de bienestar del hogar sí se asocia con la presencia y/o mayor gravedad de la anemia; se espera mayor riesgo de anemia severa en los quintiles de menor bienestar.
---

## 3. Estructura del Proyecto

```
endes-anemia2024/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias del proyecto
│
├── data/
│   ├── raw/                          # Datos originales sin procesar
│   │   └── RECH0_2024.csv
│   │   └── RECH1_2024.csv
│   │   └── RECH6_2024.csv
│   │   └── RECH23_2024.csv
│   ├── processed/                    # Datos procesados y limpios
│   │   ├── 01_data_merged.csv
│   │   ├── 02_data_cleaned.csv
│   │   └── etc
│
├── src/
│   ├── 01_read_merge.py                # Carga y fusiona módulos RECH0, RECH1, RECH23, RECH6
│   ├── 02_clean_data.py                # Filtrado,Missing values y Valores infinitos
│   ├── 03_outliers_detection.py        # Identificación y manejo de outliers
│   ├── 04_encoding.py                  # Codificación de variables categóricas
│   ├── 05_scaling.py                   # Escalado de variables numéricas
│   ├── 07_univariate_analysis.py       # Análisis univariado de variables
│   ├── 08_bivariate_analysis.py        # Análisis bivariado entre IWI y anemia
│   ├── 09_ordinal_regression.py        # Modelado de regresión ordinal para predecir niveles de anemia
│   ├── 10_clustering_pca.py            # Clustering y PCA para segmentar hogares según características socioeconómicas
│
├── doc/
│   ├── Metodologia_Anemia_ENDES.md/ 
```
---
## 4. Requisitos
- Python 3.8 o superior
- Pandas
- NumPy
- Scikit-learn
- Matplotlib  
- Seaborn
- Scipy
---
## 5. Instalación y Ejecución
5.1. Clona el repositorio: (cuando lo suba)
```bash
   git clone
 ```
5.2. Navega al directorio del proyecto:
```bash   
   cd endes-anemia2024
```
5.3. Instala las dependencias:
```bash   
   pip install -r requirements.txt   
```
5.4. Ejecuta los scripts en orden para reproducir el análisis:
```bash
   python src/01_read_merge.py
   python src/02_clean_data.py
   python src/03_outliers_detection.py
   python src/04_encoding.py
   python src/05_scaling.py
   python src/07_univariate_analysis.py
   python src/08_bivariate_analysis.py
   python src/09_ordinal_regression.py
   python src/10_clustering_pca.py
   ```
---
##  6. Metodología
### 6.1. Lectura y Unión de Datos
#### Fuentes de datos:
Se hace uso de cuatro archivos CSV:

- RECH6_2023.csv: Contiene información sobre la anemia, la edad y el sexo de los niños, y un identificador (HC60) para enlazar datos de la madre. 
- RECH0_2023.csv: Aporta datos del hogar, incluyendo variables de diseño muestral (cluster, estrato y el factor de ponderación HV005). 
- RECH23_2023.csv: Contiene información sobre la vivienda y el índice de riqueza (HV270 y HV271). 
- RECH1_2023.csv: Proporciona datos del roster familiar, en particular, la edad y el nivel educativo de la madre (renombrado como edu_sup).

#### Fusión de Datos:
Se unen los archivos utilizando la llave HHID (y HC60 para conectar datos de RECH6 y RECH1) para construir un único dataset.

### 6.2. Limpieza y Transformación de Datos
#### Filtrado:
Se seleccionan únicamente los registros de niños de 6 a 59 meses y se excluyen aquellos con valores no válidos en la variable de anemia.
#### Creación de Variables Derivadas:
- Se define la variable quintil a partir de HV270 (ya categorizado en 1 a 5). 
- Se recodifica el sexo del niño (HC27) a una variable binaria (sexo_nino). 
- Se calcula la variable peso a partir de HV005 (dividido por 1,000,000). 
- Se crea una variable binaria de anemia (anemia_bin) para análisis complementarios.
### 6.3. Modelado Estadístico
- Se ajusta un modelo de regresión ordinal logit usando OrderedModel de statsmodels (FASE 9).
- Se incluyen ponderadores derivados de HV005 para respetar el diseño muestral.
### 6.4. Interpretación de Resultados
- Si bien se tiene los resultados en formato .txt en todas las fases, aún falto desarrollar archivos .ipyn para visualizaciones y análisis más detallados.
- Pido disculpas por no tener una descripción textual sobre hallazgos interesantes o
importantes durante la exploración de los datos pero espero pueda considerar mi avance, en esta semana hábil, lo termino.
--
## 7. Contacto y Referencias
Para preguntas o sugerencias, por favor contacta a ochoaperezmilagros@outlook.com
### Referencias:
- ENDES 2024: https://www.inei.gob.pe/estadisticas/encuestas/endes/
- Documentación de statsmodels: https://www.statsmodels.org/stable/index.html
- Documentación de scikit-learn: https://scikit-learn.org/stable
---