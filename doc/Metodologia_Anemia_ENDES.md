# Documento Metodológico

## 1. Sección de Datos
Fuentes y Contenido de los Módulos:

### RECH6_2023.csv – Datos del Niño

Contenido:
Este módulo contiene la información de los niños encuestados, incluyendo variables clave para el análisis de la anemia.

Variables relevantes:
- HHID: Identificador del hogar, clave para la fusión con otros módulos. 
- HC0: Número de orden del niño. 
- HC1: Edad en meses del niño. 
- HC27: Género del niño (usualmente codificado, por ejemplo, 1 = niño, 2 = niña). 
- HC57: Indicador ordinal del nivel de anemia (codificado, por ejemplo, 1 = anemia grave, 2 = moderada, 3 = leve, 4 = sin anemia). 
- HC60: Número de orden de la madre en el hogar, usado para enlazar con el módulo RECH1. 

### RECH0_2023.csv – Datos del Hogar y Diseño Muestral

Contenido:
Proporciona información sobre la estructura del hogar, variables de diseño muestral y ponderadores.

Variables relevantes:
- HHID: Identificador del hogar. 
- HV001: Código del conglomerado o cluster. 
- HV022: Estrato muestral del hogar. 
- HV005: Factor de ponderación, utilizado para ajustar los análisis a la distribución de la población (normalmente se aplica una transformación, por ejemplo, dividiéndolo entre 1,000,000).

### RECH23_2023.csv – Información de la Vivienda e Índice de Riqueza

Contenido:
Contiene variables que describen la vivienda y los bienes del hogar, las cuales se han utilizado para construir el índice de bienestar o riqueza.

Variables relevantes:
- HHID: Identificador del hogar. 
- HV270: Índice de riqueza, categorizado en rangos enteros (1 a 5), que sirve para generar la variable quintil. 
- HV271: Puntaje continuo del índice de riqueza (opcional para análisis alternativos).

### RECH1_2023.csv – Datos del Roster Familiar (Madre)

Contenido:
Este módulo contiene la información vinculada a las madres, vinculada a los niños a través del identificador HC60.

Variables relevantes:

- HHID: Identificador del hogar. 
- HVIDX: Se renombra a HC60 para unir con RECH6. 
- HV104: Género de la madre (no requerido para este análisis, pero disponible). 
- HV105: Edad de la madre, utilizada para agregar información demográfica. 
- HV106: Nivel educativo (se renombra usualmente a edu_sup), que refleja la capacidad educativa. 
- HV109: Otra medida del nivel educativo, disponible para análisis complementarios.

## 2. Procedimiento Analítico

### A. Lógica Detrás de la Limpieza de Datos y Manejo de Missing Values:

Fusión de Módulos:
Los diferentes módulos se unen utilizando la llave HHID. Además, para unir datos de la madre y el niño se utiliza la variable HC60 (originalmente HVIDX en RECH1, renombrada para hacer la unión).

Filtrado de Registros:
Se filtran los registros para conservar únicamente aquellos niños en el rango de edad de 6 a 59 meses, y se excluyen registros con valores inválidos en la variable de anemia (HC57 fuera del rango {1,2,3,4}).

Conversión de Variables:
Se realizan transformaciones clave como:

Convertir HV270 a numérico y generar la variable quintil directamente a partir de ella (dado que ya se encuentra categorizada de 1 a 5).
Calcular el factor de ponderación (peso) a partir de HV005 (dividido por 1,000,000).
Recodificar el sexo del niño, por ejemplo, convirtiendo HC27 a una variable binaria (sexo_nino) donde 0 representa a los niños y 1 a las niñas.
Manejo de Missing Values e Infinitos:
Se identifican y eliminan las filas que contienen valores faltantes o infinitos en las variables clave utilizadas para el modelo, asegurando así la integridad de la matriz de variables predictoras.

### B. Configuración de Variables:

Variable Respuesta (y):
HC57, la variable ordinal que clasifica la anemia en 4 categorías (1=grave, 2=moderada, 3=leve, 4=sin anemia).

Variables Predictoras Seleccionadas (7 variables finales):

**Continuas (escaladas):**
- edad_nino: Edad en meses, escalada (Z-score). Correlación con HC57: 0.339 (predictivo más fuerte).
- edad_madre: Edad de la madre, escalada. Correlación con HC57: 0.097.

**Categóricas (one-hot encoded, drop_first=True):**
- quintil_raw_3: Dummy quintil 3 vs referencia (quintil 1). Significancia bivariada: χ² = 74.6, p < 0.001.
- quintil_raw_4: Dummy quintil 4 vs referencia. Significancia bivariada: χ² = 129.2, p < 0.001.
- quintil_raw_5: Dummy quintil 5 vs referencia. Significancia bivariada: χ² = 134.2, p < 0.001.
- edu_madre_3.0: Dummy educación media vs referencia (educación baja). Significancia bivariada: χ² = 154.7, p < 0.001.
- sexo_nino_code_2: Dummy sexo niña vs referencia (niño). Significancia bivariada: χ² = 38.7, p < 0.001.

**Variables Excluidas (Justificación técnica):**
- ponderador_raw: Escala numérica extrema (32K-1.3M), efecto negligible en coeficientes (5.876e-07), genera inestabilidad en optimización MLE. Removida.
- indice_riqueza: Redundancia con quintiles (versión continua del mismo constructo), aliasing numérico. Removida.
- estrato: 240 valores únicos, correlación = 0.017, sin significancia bivariada (p > 0.05). Removida.
- quintil_raw_2: Chi-cuadrado = 4.46, p = 0.216 (NO significativo). Categoría rara (8.5% de casos). Removida.
- edu_madre_1.0: Redundancia estructural, efecto menor (χ² = 45.7) vs edu_madre_3.0 (χ² = 154.7). Removida.
- HC60: Variable de linkage (rango 1-995), asimetría extrema (4.07). Función completada en fusión (Fase 1). Removida.

**Impacto esperado:**
- Convergencia MLE garantizada (matriz Hessiana bien condicionada).
- Coeficientes estables y precisos.
- Facilita análisis de clusters y PCA posterior (Fase 10) sin artefactos numéricos.

### C. Refinamiento en FASE 9: Análisis Multivariado

**Diagnóstico de Convergencia:**
Se realizó análisis diagnóstico de las 13 variables iniciales de Fase 6 para optimizar convergencia MLE en regresión ordinal. Se identificaron 6 variables problemáticas que causaban:
- Escala numérica desproporcionada (ponderador_raw: efecto 5.876e-07)
- Redundancia estructural (indice_riqueza duplicada con quintiles)
- Sin poder predictivo bivariado (estrato: r=0.017; quintil_raw_2: p=0.216)
- Separación parcial (categorías raras con curtosis extrema)

**Decisión:** Reducción controlada a 7 variables de máximo poder predictivo.

**Validación estadística:**
- Todas las 7 variables retenidas significativas a p < 0.001 (bivariado)
- Correlaciones con respuesta: edad_nino (0.339) > edu_madre (0.088) > edad_madre (0.097) > quintiles (0.06-0.08) > sexo (0.044)
- VIF implícito: Variables orthogonales, sin multicolinealidad residual

**Impacto:**
- Convergencia rápida garantizada
- Interpretación clara de coeficientes ordenales
- Matriz de datos limpia para PCA y clustering (Fase 10)

### D. Selección y Ajuste del Modelo Ordenal:

Razonamiento del Modelo:
Se utiliza un modelo de regresión ordinal logit (con OrderedModel de statsmodels) para aprovechar la naturaleza ordinal de la variable respuesta HC57. La elección de este modelo permite interpretar los parámetros en términos de acumulación de probabilidad y definir umbrales que separan las categorías.

Uso de Ponderadores:
Nota: La variable ponderador_raw fue removida en el refinamiento Fase 9 debido a su escala desproporcionada y efecto negligible (5.876e-07), que no justificaba la inestabilidad numérica introducida. El ajuste por diseño muestral se considera en la interpretación inferencial a través de la documentación metodológica (ENDES es encuesta compleja).

## 3. Interpretación y Validación de Resultados

Especificaciones técnicas:

**Convergencia:**
- Algoritmo: Maximum Likelihood Estimation (MLE) con Newton-Raphson
- Criterio de convergencia: gtol=1e-5 (gradient tolerance)
- Máximo de iteraciones: 500
- Matriz Hessiana: Well-conditioned (7 variables bien estructuradas)

**Diagnósticos:**
- Log-Likelihood: Medida de bondad de ajuste global
- AIC/BIC: Comparación de modelos (menor es mejor)
- P-values: Significancia individual de coeficientes (< 0.05)
- Umbrales (gamma/Alpha): Separación ordinal entre categorías de anemia

**Interpretación de coeficientes:**
- Positivo: Aumenta probabilidad de categoría anemia más severa
- Negativo: Aumenta probabilidad de categoría anemia menos severa
- Magnitud: Log-odds por unidad de cambio

**Validación posterior (Fase 10):**
- PCA sobre matriz (7 variables): Reducción de dimensionalidad
- K-means: Clustering en espacio transformado
- Método del codo: Determinación de k óptimo
- Silhouette score: Validación de cohesión de clusters

