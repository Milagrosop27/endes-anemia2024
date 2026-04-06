# Análisis ENDES 2024

#### Pregunta de Investigación
**¿Se asocia el índice de bienestar del hogar con la severidad de la anemia en niños peruanos de 6-59 meses?**


---

##  Estructura

```
src/        8 scripts de producción (01-06 preprocesamiento, 09-10 modelos)
notebooks/  5 notebooks de análisis (00 maestro, 07-10 visualización)
  doc/      Metodología
```
---
---

##  Ejecutar

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ochoaperezmilagros/endes-anemia2024/blob/main/notebooks/00_ANALISIS_MAESTRO.ipynb)

O localmente:
```bash
git clone https://github.com/Milagrosop27/endes-anemia2024.git
pip install -r requirements.txt
jupyter notebook notebooks/00_ANALISIS_MAESTRO.ipynb
```

---

##  Datos & Metodología

#### Muestra
- **N**: 16,426 niños
- **Respuesta**: Severidad de anemia (4 categorías ordinales)
- **Predictores**: 7 variables optimizadas

#### Pipeline de Análisis

```
Datos Crudos → Fusión & Limpieza → Preprocesamiento → 
Exploratorio → Multivariado → Segmentación → Hallazgos
```

#### Métodos: χ² | Spearman | Regresión Ordinal | PCA + K-means


## Referencias
- ENDES 2024: https://www.inei.gob.pe/estadisticas/encuestas/endes/
- Documentación de statsmodels: https://www.statsmodels.org/stable/index.html
- Documentación de scikit-learn: https://scikit-learn.org/stable
