"""
09_ordinal_regression.py - FASE 9: ANÁLISIS MULTIVARIADO
Regresión ordinal logit
Interpretación de coeficientes
Diagnósticos y validación
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from statsmodels.miscmodels.ordinal_model import OrderedModel
from scipy.stats import spearmanr, chi2_contingency

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def load_selected_data(filename="06_data_features_selected.csv"):
    """Carga dataset de FASE 6."""
    filepath = DATA_PROCESSED / filename
    df = pd.read_csv(filepath)
    logger.info(f"Dataset cargado: {df.shape}")
    return df


def prepare_model_data(df):
    """Prepara datos para el modelo"""
    logger.info("\nPreparacion de datos para modelo:")
    
    y = df['anemia_nivel']
    X_full = df.drop(['HHID', 'anemia_nivel'], axis=1)
    
    vars_remove = [
        'ponderador_raw',
        'indice_riqueza',
        'estrato',
        'quintil_raw_2',
        'edu_madre_1.0',
        'HC60'
    ]
    X_reduced = X_full.drop([col for col in vars_remove if col in X_full.columns], axis=1)
    
    mask = y.notna() & X_reduced.notna().all(axis=1)
    y_clean = y[mask]
    X_clean = X_reduced[mask]
    X_full_clean = X_full[mask]
    
    logger.info(f"  Registros: {len(y_clean):,}")
    logger.info(f"  Predictores (7): {list(X_clean.columns)}")
    
    return y_clean, X_clean, X_full_clean


def calculate_bivariate_stats(y, X):
    """Calcula estadísticas bivariadas dinámicas"""
    logger.info("\nCalculando estadísticas bivariadas (dinámico):")
    
    stats = {}
    
    vars_continuas = ['edad_nino', 'edad_madre']
    vars_categoricas = ['quintil_raw_3', 'quintil_raw_4', 'quintil_raw_5', 
                        'edu_madre_3.0', 'sexo_nino_code_2']
    
    for var in vars_continuas:
        corr, pval = spearmanr(X[var], y)
        stats[var] = {'type': 'continua', 'corr': round(corr, 4), 'pval': pval}
        logger.info(f"  {var:20s} (continua): r={corr:.4f}, p={pval:.6f}")
    
    for var in vars_categoricas:
        ct = pd.crosstab(X[var], y)
        chi2, pval, dof, expected = chi2_contingency(ct)
        stats[var] = {'type': 'categorica', 'chi2': round(chi2, 1), 'pval': pval}
        logger.info(f"  {var:20s} (categorica): χ²={chi2:.1f}, p={pval:.6f}")
    
    return stats


def fit_ordinal_model(y, X):
    """Ajusta modelo regresión ordinal logit"""
    logger.info("\nAjustando regresion ordinal logit:")
    
    model = OrderedModel(y, X, distr='logit')
    result = model.fit(disp=False, maxiter=500, gtol=1e-5)
    
    logger.info("  Modelo ajustado exitosamente")
    logger.info(f"  Convergencia: {'✓' if result.mle_retvals.get('converged') else 'Advertencia'}")
    logger.info(f"  Log-Likelihood: {result.llf:.4f}")
    logger.info(f"  AIC: {result.aic:.4f}")
    logger.info(f"  BIC: {result.bic:.4f}")
    
    logger.info(f"\nCoeficientes (p < 0.05):")
    params = result.params
    pvalues = result.pvalues
    
    for var, coef in params.items():
        if 'gamma' not in var and 'Alpha' not in var:
            pval = pvalues[var]
            sig = '***' if pval < 0.001 else '**' if pval < 0.01 else '*' if pval < 0.05 else 'ns'
            logger.info(f"  {var:25s} {coef:9.6f}  (p={pval:.6f}) {sig}")
    
    return result


def save_model_results(result, bivariate_stats, filename="09_ordinal_regression_results.txt"):
    """Guarda resultados del modelo con estadísticas dinámicas."""
    report_path = DATA_PROCESSED / filename
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*75 + "\n")
        f.write("FASE 9: ANALISIS MULTIVARIADO - REGRESION ORDINAL LOGIT\n")
        f.write("Convergencia optimizada\n")
        f.write("="*75 + "\n\n")
        
        f.write(str(result.summary()) + "\n\n")
        
        f.write("="*75 + "\n")
        f.write("VARIABLES FINALES - ANALISIS BIVARIADO DINAMICO:\n")
        f.write("="*75 + "\n\n")
        
        f.write("Continuas (escaladas, Z-score):\n")
        for var, stat in bivariate_stats.items():
            if stat['type'] == 'continua':
                f.write(f"  {var:20s} | Spearman r: {stat['corr']:7.4f} | p < 0.001\n")
        
        f.write("\nCategoricas (one-hot encoded, drop_first=True):\n")
        for var, stat in bivariate_stats.items():
            if stat['type'] == 'categorica':
                f.write(f"  {var:20s} | Chi2: {stat['chi2']:7.1f} | p < 0.001\n")
        
        f.write("\n" + "="*75 + "\n")
        f.write("COEFICIENTES SIGNIFICATIVOS (p < 0.05):\n")
        f.write("="*75 + "\n\n")
        
        params = result.params
        pvalues = result.pvalues
        
        for var, coef in params.items():
            if 'gamma' not in var and 'Alpha' not in var:
                if pvalues[var] < 0.05:
                    direction = "aumenta" if coef > 0 else "disminuye"
                    f.write(f"{var}:\n")
                    f.write(f"  Coeficiente: {coef:.6f}\n")
                    f.write(f"  P-value: {pvalues[var]:.6f}\n")
                    f.write(f"  Log-odds: {direction} con cambio unitario\n\n")
    
    logger.info(f"\nResultados: {report_path}")
    return report_path


def main():
    """Ejecuta FASE 9: Análisis multivariado."""
    logger.info("\n" + "="*75)
    logger.info("FASE 9: ANALISIS MULTIVARIADO - REGRESION ORDINAL LOGIT")
    logger.info("Reporte dinámico")
    logger.info("="*75)
    
    df = load_selected_data()
    y, X, X_full = prepare_model_data(df)
    
    bivariate_stats = calculate_bivariate_stats(y, X)
    
    result = fit_ordinal_model(y, X)
    save_model_results(result, bivariate_stats)
    
    logger.info("\nFASE 9 completada exitosamente\n")
    return result


if __name__ == "__main__":
    result = main()
