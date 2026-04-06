"""
01_read_merge.py - FASE 1: LECTURA E INTEGRACIÓN DE MÓDULOS ENDES 2024
Carga y fusiona módulos RECH0, RECH1, RECH23, RECH6
Output: data/processed/01_data_merged.csv
"""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_PROCESSED.mkdir(exist_ok=True, parents=True)


def read_modules():
    """Lee los cuatro módulos RECH necesarios."""
    logger.info("Leyendo módulos RECH...")

    rech6 = pd.read_csv(DATA_RAW / "RECH6_2024.csv",
                        usecols=['HHID', 'HC0', 'HC1', 'HC27', 'HC57', 'HC60'])
    logger.info(f"RECH6 cargado: {rech6.shape}")

    rech0 = pd.read_csv(DATA_RAW / "RECH0_2024.csv",
                        usecols=['HHID', 'HV001', 'HV022', 'HV005'])
    logger.info(f"RECH0 cargado: {rech0.shape}")

    rech23 = pd.read_csv(DATA_RAW / "RECH23_2024.csv",
                         usecols=['HHID', 'HV270', 'HV271'])
    logger.info(f"RECH23 cargado: {rech23.shape}")

    rech1 = pd.read_csv(DATA_RAW / "RECH1_2024.csv",
                        usecols=['HHID', 'HVIDX', 'HV104', 'HV105', 'HV106', 'HV109'])
    logger.info(f"RECH1 cargado: {rech1.shape}")

    return rech6, rech0, rech23, rech1


def merge_modules(rech6, rech0, rech23, rech1):
    """Fusiona los cuatro módulos RECH en un único DataFrame."""
    logger.info("Fusionando módulos...")

    df = rech6.merge(rech0, on='HHID', how='left')
    df = df.merge(rech23, on='HHID', how='left')
    logger.info(f"Fusión RECH6+RECH0+RECH23: {df.shape}")

    madre = rech1.rename(columns={'HVIDX': 'HC60'})
    df = df.merge(madre[['HHID', 'HC60', 'HV104', 'HV105', 'HV106', 'HV109']],
                  on=['HHID', 'HC60'], how='left')
    logger.info(f"Fusión final con RECH1: {df.shape}")

    return df


def rename_columns(df):
    """Renombra columnas para claridad interpretativa."""
    rename_dict = {
        'HC1': 'edad_nino',
        'HC27': 'sexo_nino_code',
        'HC57': 'anemia_nivel',
        'HC0': 'num_nino',
        'HV001': 'cluster',
        'HV022': 'estrato',
        'HV005': 'ponderador_raw',
        'HV270': 'quintil_raw',
        'HV271': 'indice_riqueza',
        'HV104': 'sexo_madre_code',
        'HV105': 'edad_madre',
        'HV106': 'edu_madre',
        'HV109': 'edu_madre_det'
    }
    df = df.rename(columns=rename_dict)
    logger.info("Columnas renombradas")
    return df


def save_merged_data(df, filename="01_data_merged.csv"):
    """Guarda el DataFrame integrado en CSV."""
    output_path = DATA_PROCESSED / filename
    df.to_csv(output_path, index=False, encoding='utf-8')
    logger.info(f"Dataset guardado: {output_path}")
    return output_path

def main():
    """Ejecuta la lectura, fusión y guardado de datos."""
    logger.info("\n" + "="*70)
    logger.info("FASE 1: LECTURA E INTEGRACIÓN DE MÓDULOS ENDES 2024")
    logger.info("="*70)

    rech6, rech0, rech23, rech1 = read_modules()
    df = merge_modules(rech6, rech0, rech23, rech1)
    df = rename_columns(df)

    logger.info(f"\nDimensiones finales: {df.shape[0]:,} registros x {df.shape[1]} columnas")

    output_path = save_merged_data(df)
    logger.info("FASE 1 completada\n")

    return df, output_path


if __name__ == "__main__":
    df_merged, output_file = main()
