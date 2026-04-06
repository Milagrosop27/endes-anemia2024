"""
FASE 4: CODIFICACIÓN DE VARIABLES CATEGÓRICAS
One-hot encoding para variables categóricas
Prevención de multicolinealidad (drop_first=True)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def load_outliers_handled_data(filename="03_data_cleaned_outliers_handled.csv"):
    filepath = DATA_PROCESSED / filename
    df = pd.read_csv(filepath)
    logger.info(f"Datos cargados: {df.shape}")
    return df


def encode_categorical_variables(df):
    logger.info("\nCodificación de variables categóricas:")
    
    vars_to_encode = {
        'HV270': 'quintil_raw',
        'HV106': 'edu_madre',
        'HC27': 'sexo_nino_code'
    }
    
    df_encoded = df.copy()
    
    for original_col, new_prefix in vars_to_encode.items():
        if original_col in df_encoded.columns:
            dummies = pd.get_dummies(df_encoded[original_col], 
                                     prefix=new_prefix, 
                                     drop_first=True)
            df_encoded = pd.concat([df_encoded, dummies], axis=1)
            logger.info(f"  {original_col}: {dummies.shape[1]} dummies creadas (drop_first=True)")
    
    return df_encoded


def main():
    logger.info("\n" + "="*70)
    logger.info("FASE 4: CODIFICACIÓN DE VARIABLES CATEGÓRICAS")
    logger.info("="*70)
    
    df = load_outliers_handled_data()
    
    df_encoded = encode_categorical_variables(df)
    
    logger.info(f"\nRegistros: {df_encoded.shape[0]:,}")
    logger.info(f"Columnas: {df_encoded.shape[1]} (antes: {df.shape[1]})")
    
    output_file = DATA_PROCESSED / "04_data_encoded.csv"
    df_encoded.to_csv(output_file, index=False)
    
    report_file = DATA_PROCESSED / "04_encoding_report.txt"
    with open(report_file, 'w') as f:
        f.write("FASE 4: CODIFICACIÓN\n")
        f.write("="*70 + "\n\n")
        f.write(f"Registros: {df_encoded.shape[0]:,}\n")
        f.write(f"Columnas originales: {df.shape[1]}\n")
        f.write(f"Columnas finales: {df_encoded.shape[1]}\n\n")
        f.write("Método: One-hot encoding (drop_first=True)\n")
        f.write("Variables codificadas: HV270, HV106, HC27\n")
    
    logger.info(f"\nFase 4 completada: {output_file}")
    return df_encoded


if __name__ == "__main__":
    main()

