"""
FASE 5: ESCALAMIENTO DE DATOS
Normalización/estandarización de variables continuas
Método: Z-score (StandardScaler)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def load_encoded_data(filename="04_data_encoded.csv"):
    filepath = DATA_PROCESSED / filename
    df = pd.read_csv(filepath)
    logger.info(f"Datos cargados: {df.shape}")
    return df


def scale_continuous_variables(df):
    logger.info("\nEscalamiento Z-score:")
    
    vars_to_scale = ['HC1', 'HV105', 'HV271']
    vars_to_scale = [col for col in vars_to_scale if col in df.columns]
    
    df_scaled = df.copy()
    scaler = StandardScaler()
    
    df_scaled[vars_to_scale] = scaler.fit_transform(df[vars_to_scale])
    
    for col in vars_to_scale:
        logger.info(f"  {col}: media={df_scaled[col].mean():.4f}, std={df_scaled[col].std():.4f}")
    
    return df_scaled


def main():
    logger.info("\n" + "="*70)
    logger.info("FASE 5: ESCALAMIENTO DE DATOS")
    logger.info("="*70)
    
    df = load_encoded_data()
    
    df_scaled = scale_continuous_variables(df)
    
    logger.info(f"\nRegistros: {df_scaled.shape[0]:,}")
    logger.info(f"Columnas: {df_scaled.shape[1]}")
    
    output_file = DATA_PROCESSED / "05_data_scaled.csv"
    df_scaled.to_csv(output_file, index=False)
    
    report_file = DATA_PROCESSED / "05_scaling_report.txt"
    with open(report_file, 'w') as f:
        f.write("FASE 5: ESCALAMIENTO\n")
        f.write("="*70 + "\n\n")
        f.write(f"Registros: {df_scaled.shape[0]:,}\n")
        f.write(f"Columnas: {df_scaled.shape[1]}\n\n")
        f.write("Método: Z-score (StandardScaler)\n")
        f.write("Variables escaladas: HC1, HV105, HV271\n\n")
        f.write("Estadísticas post-escalamiento:\n")
        for col in ['HC1', 'HV105', 'HV271']:
            if col in df_scaled.columns:
                f.write(f"  {col}: media={df_scaled[col].mean():.4f}, std={df_scaled[col].std():.4f}\n")
    
    logger.info(f"\nFase 5 completada: {output_file}")
    return df_scaled


if __name__ == "__main__":
    main()

