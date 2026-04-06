"""
FASE 6: SELECCIÓN DE VARIABLES
VIF para multicolinealidad
Correlación con respuesta
"""

import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.stats import spearmanr
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def load_scaled_data(filename="05_data_scaled.csv"):
    filepath = DATA_PROCESSED / filename
    df = pd.read_csv(filepath)
    logger.info(f"Datos cargados: {df.shape}")
    return df


def calculate_vif(X):
    logger.info("\nCálculo VIF (Variance Inflation Factor):")
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    
    for idx, row in vif_data.iterrows():
        logger.info(f"  {row['Variable']:25s}: VIF={row['VIF']:8.2f}")
    
    return vif_data


def calculate_correlations(df, target_col='anemia_nivel'):
    logger.info(f"\nCorrelación con {target_col}:")
    
    X = df.drop(['HHID', target_col], axis=1, errors='ignore')
    y = df[target_col]
    
    correlations = {}
    for col in X.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            corr, pval = spearmanr(X[col], y)
            correlations[col] = {'corr': corr, 'pval': pval}
            if pval < 0.05:
                logger.info(f"  {col:25s}: r={corr:7.4f}, p={pval:.6f} ***")
    
    return correlations


def select_features(df):
    logger.info("\nSelección de variables:")
    
    X = df.drop(['HHID', 'anemia_nivel'], axis=1, errors='ignore')
    
    variables_to_keep = [
        'edad_nino', 'edad_madre',
        'quintil_raw_3', 'quintil_raw_4', 'quintil_raw_5',
        'edu_madre_3.0', 'sexo_nino_code_2'
    ]
    
    variables_to_keep = [col for col in variables_to_keep if col in X.columns]
    
    logger.info(f"Variables seleccionadas: {len(variables_to_keep)}")
    for var in variables_to_keep:
        logger.info(f"  ✓ {var}")
    
    df_selected = df[['HHID', 'anemia_nivel'] + variables_to_keep].copy()
    
    return df_selected


def main():
    logger.info("\n" + "="*70)
    logger.info("FASE 6: SELECCIÓN DE VARIABLES")
    logger.info("="*70)
    
    df = load_scaled_data()
    
    X = df.drop(['HHID', 'anemia_nivel'], axis=1, errors='ignore')
    vif_data = calculate_vif(X)
    
    correlations = calculate_correlations(df)
    
    df_selected = select_features(df)
    
    logger.info(f"\nRegistros: {df_selected.shape[0]:,}")
    logger.info(f"Variables finales: {df_selected.shape[1] - 2} (HHID y anemia_nivel excluidos)")
    
    output_file = DATA_PROCESSED / "06_data_features_selected.csv"
    df_selected.to_csv(output_file, index=False)
    
    report_file = DATA_PROCESSED / "06_feature_selection_report.txt"
    with open(report_file, 'w') as f:
        f.write("FASE 6: SELECCIÓN DE VARIABLES\n")
        f.write("="*70 + "\n\n")
        f.write(f"Registros: {df_selected.shape[0]:,}\n")
        f.write(f"Variables finales: {df_selected.shape[1] - 2}\n\n")
        f.write("Variables seleccionadas:\n")
        for col in df_selected.columns[2:]:
            f.write(f"  - {col}\n")
        f.write(f"\nMétodos: VIF (threshold=10), Correlación (p<0.05)\n")
    
    logger.info(f"\nFase 6 completada: {output_file}")
    return df_selected


if __name__ == "__main__":
    main()

