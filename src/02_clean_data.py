"""
02_clean_data.py - FASE 2: LIMPIEZA DE DATOS
Filtrado: HC1 ∈ [6-59], HC57 ∈ {1,2,3,4}
Missing values: identificar y documentar
Valores infinitos: tratar o eliminar
Output: data/processed/02_data_cleaned.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def load_merged_data(filename="01_data_merged.csv"):
    """Carga dataset de FASE 1."""
    filepath = DATA_PROCESSED / filename
    df = pd.read_csv(filepath)
    logger.info(f"Dataset cargado: {df.shape}")
    return df


def handle_infinite_values(df):
    """Reemplaza valores infinitos por NaN."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    inf_count = 0

    for col in numeric_cols:
        col_inf = np.isinf(df[col]).sum()
        if col_inf > 0:
            inf_count += col_inf
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)

    if inf_count > 0:
        logger.warning(f"Valores infinitos reemplazados: {inf_count}")
    return df


def apply_filters(df):
    """Aplica filtros: HC1 ∈ [6-59], HC57 ∈ {1,2,3,4}"""
    initial_rows = len(df)

    mask_edad = (df['edad_nino'] >= 6) & (df['edad_nino'] <= 59)
    mask_anemia = df['anemia_nivel'].isin([1, 2, 3, 4])

    removed_edad = (~mask_edad).sum()
    removed_anemia = (~mask_anemia).sum()

    df = df[mask_edad & mask_anemia].reset_index(drop=True)

    final_rows = len(df)
    removed_total = initial_rows - final_rows
    pct_removed = (removed_total / initial_rows) * 100

    logger.info(f"Filtrados: {removed_total:,} registros ({pct_removed:.2f}%)")
    logger.info(f"  edad_nino [6-59]: {removed_edad:,} removidos")
    logger.info(f"  anemia_nivel {{1,2,3,4}}: {removed_anemia:,} removidos")
    logger.info(f"Registros finales: {final_rows:,}")

    return df


def analyze_missing(df):
    """Analiza y documenta missing values."""
    logger.info("\nAnalisis de Missing Values:")

    missing_analysis = {}
    for col in df.columns:
        n_missing = df[col].isnull().sum()
        pct_missing = (n_missing / len(df)) * 100
        missing_analysis[col] = {'count': n_missing, 'pct': pct_missing}

        if n_missing > 0:
            logger.info(f"  {col:20s}: {n_missing:7,} ({pct_missing:6.2f}%)")

    return missing_analysis


def save_cleaned_data(df, missing_analysis, filename="02_data_cleaned.csv"):
    """Guarda dataset limpio y reporte."""
    output_path = DATA_PROCESSED / filename
    df.to_csv(output_path, index=False, encoding='utf-8')
    logger.info(f"\nDataset limpio guardado: {output_path}")

    report_path = DATA_PROCESSED / "02_cleaning_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("REPORTE DE LIMPIEZA - FASE 2\n")
        f.write("="*70 + "\n\n")
        f.write(f"Registros finales: {len(df):,}\n")
        f.write(f"Columnas: {df.shape[1]}\n\n")
        f.write("MISSING VALUES:\n")
        f.write("-"*70 + "\n")
        for col, info in missing_analysis.items():
            if info['count'] > 0:
                f.write(f"{col:20s}: {info['count']:7,} ({info['pct']:6.2f}%)\n")

    logger.info(f"Reporte guardado: {report_path}")
    return output_path


def main():
    """Ejecuta FASE 2: Limpieza de datos."""
    logger.info("\n" + "="*70)
    logger.info("FASE 2: LIMPIEZA DE DATOS")
    logger.info("="*70)

    df = load_merged_data()
    df = handle_infinite_values(df)
    df = apply_filters(df)
    missing_analysis = analyze_missing(df)
    save_cleaned_data(df, missing_analysis)

    logger.info("FASE 2 completada\n")
    return df


if __name__ == "__main__":
    df_cleaned = main()
