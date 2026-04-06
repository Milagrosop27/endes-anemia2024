"""
FASE 3: DETECCIÓN DE OUTLIERS
Identificación y manejo de valores atípicos
Métodos: IQR, Z-score
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def load_cleaned_data(filename="02_data_cleaned.csv"):
    filepath = DATA_PROCESSED / filename
    df = pd.read_csv(filepath)
    logger.info(f"Datos cargados: {df.shape}")
    return df


def detect_outliers_iqr(df, columns):
    logger.info("\nDetección IQR:")
    outliers_mask = pd.Series([False] * len(df))
    
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            col_outliers = (df[col] < lower) | (df[col] > upper)
            count = col_outliers.sum()
            
            logger.info(f"  {col}: {count} outliers ({count/len(df)*100:.2f}%)")
            outliers_mask |= col_outliers
    
    return outliers_mask


def detect_outliers_zscore(df, columns, threshold=3):
    logger.info(f"\nDetección Z-score (threshold={threshold}):")
    outliers_mask = pd.Series([False] * len(df))
    
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            col_outliers = z_scores > threshold
            count = col_outliers.sum()
            
            logger.info(f"  {col}: {count} outliers ({count/len(df)*100:.2f}%)")
            outliers_mask |= col_outliers
    
    return outliers_mask


def handle_outliers_winsorize(df, columns, limits=0.05):
    logger.info(f"\nWinsorización (límites={limits}):")
    df_winsorized = df.copy()
    
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            lower = df[col].quantile(limits)
            upper = df[col].quantile(1 - limits)
            df_winsorized[col] = df[col].clip(lower=lower, upper=upper)
            logger.info(f"  {col}: clipped [{lower:.2f}, {upper:.2f}]")
    
    return df_winsorized


def main():
    logger.info("\n" + "="*70)
    logger.info("FASE 3: DETECCIÓN Y MANEJO DE OUTLIERS")
    logger.info("="*70)
    
    df = load_cleaned_data()
    
    numeric_cols = ['edad_nino', 'edad_madre', 'HC1', 'HV105', 'HV271']
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    outliers_iqr = detect_outliers_iqr(df, numeric_cols)
    outliers_zscore = detect_outliers_zscore(df, numeric_cols)
    
    logger.info(f"\nTotal outliers (IQR): {outliers_iqr.sum()} ({outliers_iqr.sum()/len(df)*100:.2f}%)")
    logger.info(f"Total outliers (Z-score): {outliers_zscore.sum()} ({outliers_zscore.sum()/len(df)*100:.2f}%)")
    
    df_handled = handle_outliers_winsorize(df, numeric_cols, limits=0.05)
    
    output_file = DATA_PROCESSED / "03_data_cleaned_outliers_handled.csv"
    df_handled.to_csv(output_file, index=False)
    
    report_file = DATA_PROCESSED / "03_outliers_report.txt"
    with open(report_file, 'w') as f:
        f.write("FASE 3: DETECCIÓN DE OUTLIERS\n")
        f.write("="*70 + "\n\n")
        f.write(f"Registros procesados: {len(df):,}\n")
        f.write(f"Outliers IQR: {outliers_iqr.sum()} ({outliers_iqr.sum()/len(df)*100:.2f}%)\n")
        f.write(f"Outliers Z-score: {outliers_zscore.sum()} ({outliers_zscore.sum()/len(df)*100:.2f}%)\n\n")
        f.write("Método aplicado: Winsorización (limits=0.05)\n")
        f.write("Output: 03_data_cleaned_outliers_handled.csv\n")
    
    logger.info(f"\nFase 3 completada: {output_file}")
    return df_handled


if __name__ == "__main__":
    main()

