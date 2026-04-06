# Análisis de Anemia ENDES 2024

### Pregunta de Investigación
**¿Se asocia el índice de bienestar del hogar con la severidad de la anemia en niños peruanos de 6-59 meses?**

### Hallazgo Clave
**Asociación Espuria**: Significativa a nivel bivariado (χ²=134, p<0.001) pero **confundida por edad del niño**. Después del ajuste multivariado, la asociación desaparece.

**Implicación de Política**: Intervenir sobre edad (suplementación), no sobre pobreza.

---

##  Inicio Rápido

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ochoaperezmilagros/endes-anemia2024/blob/main/notebooks/00_ANALISIS_MAESTRO.ipynb)

---

##  Datos & Metodología

### Muestra
- **Fuente**: ENDES 2024
- **N**: 16,426 niños
- **Respuesta**: Severidad de anemia (4 categorías ordinales)
- **Predictores**: 7 variables optimizadas

### Pipeline de Análisis

```
Datos Crudos → Fusión & Limpieza → Preprocesamiento → 
Exploratorio → Multivariado → Segmentación → Hallazgos
```

### Métodos: χ² | Spearman | Regresión Ordinal | PCA + K-means
### Revisar Metodología en /doc/metodologia.md

---

##  Estructura

```
src/        8 scripts de producción (01-06 preprocesamiento, 09-10 modelos)
notebooks/  5 notebooks de análisis (00 maestro, 07-10 visualización)
doc/        Documentación técnica
```

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

## Resultados

| Fase | Hallazgo |
|------|----------|
| **8** | Asociación riqueza-anemia: χ² = 134.2, p < 0.001 |
| **9** | Efecto desaparece al ajustar por edad (confundimiento) |
| **10** | 3 clusters: diferenciados por edad, no por riqueza |

---

## Referencias
- ENDES 2024: https://www.inei.gob.pe/estadisticas/encuestas/endes/
- Documentación de statsmodels: https://www.statsmodels.org/stable/index.html
- Documentación de scikit-learn: https://scikit-learn.org/stable
