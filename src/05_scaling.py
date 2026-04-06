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
import pickle

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


def load_encoded_data(filename="04_data_encoded.csv"):
    """Carga datos codificados de la Fase 4"""
    filepath = DATA_PROCESSED / filename
    
    if not filepath.exists():
        logger.error(f"Archivo no encontrado: {filepath}")
        raise FileNotFoundError(f"Archivo requerido: {filepath}")
    
    df = pd.read_csv(filepath)
    logger.info(f"✓ Datos cargados: {df.shape[0]:,} registros × {df.shape[1]} columnas")
    return df

def scale_continuous_variables(df):
    """Escala variables continuas usando Z-score"""
    logger.info("\nEscalamiento Z-score:")

    # COLUMNAS CORRECTAS PARA ENDES (actualizado)
    vars_to_scale = ['edad_nino', 'HC60', 'indice_riqueza', 'edad_madre', 'edu_madre', 'edu_madre_det']
    
    # Filtrar solo las que existen en el dataset
    vars_to_scale = [col for col in vars_to_scale if col in df.columns]
    
    if not vars_to_scale:
        logger.error("No hay variables numéricas para escalar")
        logger.error(f"Columnas disponibles: {df.columns.tolist()}")
        raise ValueError("No hay variables válidas para escalar")
    
    logger.info(f"Variables a escalar ({len(vars_to_scale)}): {', '.join(vars_to_scale)}")
    
    df_scaled = df.copy()

    # Reemplazar valores infinitos
    for col in vars_to_scale:
        inf_count = np.isinf(df_scaled[col]).sum()
        if inf_count > 0:
            logger.warning(f"  ⚠ {col}: {inf_count} valores infinitos detectados")
        df_scaled[col] = df_scaled[col].replace([np.inf, -np.inf], np.nan)
    
    # Eliminar registros con NaN en variables a escalar
    registros_antes = len(df_scaled)
    
    df_scaled = df_scaled.dropna(subset=vars_to_scale)
    registros_eliminados = registros_antes - len(df_scaled)
    
    if registros_eliminados > 0:
        pct = (registros_eliminados / registros_antes) * 100
        logger.warning(f"  ⚠ {registros_eliminados:,} registros eliminados ({pct:.2f}%)")
    else:
        logger.info(f"  ✓ No hay valores faltantes")
    
    # Aplicar StandardScaler
    logger.info(f"  Aplicando StandardScaler...")
    scaler = StandardScaler()
        try:
        df_scaled[vars_to_scale] = scaler.fit_transform(df_scaled[vars_to_scale].astype(float))
        logger.info(f"  ✓ Escalamiento completado exitosamente")
    except Exception as e:
        logger.error(f"  Error en StandardScaler: {str(e)}")
        raise
    
    # Mostrar estadísticas
    logger.info(f"\nEstadísticas post-escalamiento:")
    for col in vars_to_scale:
        mean_val = df_scaled[col].mean()
        std_val = df_scaled[col].std()
        logger.info(f"  {col}: media={mean_val:.6f}, std={std_val:.6f}")
    
    return df_scaled, scaler


def main():
    logger.info("\n" + "="*70)
    logger.info("FASE 5: ESCALAMIENTO DE DATOS")
    logger.info("="*70)
    try:
        df = load_encoded_data()
        
        df_scaled, scaler = scale_continuous_variables(df)
        
        logger.info(f"\n✓ Registros finales: {df_scaled.shape[0]:,}")
        logger.info(f"✓ Columnas: {df_scaled.shape[1]}")
        
        # Guardar datos escalados
        output_file = DATA_PROCESSED / "05_data_scaled.csv"
        df_scaled.to_csv(output_file, index=False)
        logger.info(f"\n✓ CSV guardado: {output_file}")
        
        # Guardar scaler para reproducibilidad
        scaler_file = DATA_PROCESSED / "05_scaler.pkl"
        with open(scaler_file, 'wb') as f:
            pickle.dump(scaler, f)
        logger.info(f"✓ Scaler guardado: {scaler_file}")
        
        # Generar reporte
        report_file = DATA_PROCESSED / "05_scaling_report.txt"
        with open(report_file, 'w') as f:
            f.write("FASE 5: ESCALAMIENTO DE DATOS\n")
            f.write("="*70 + "\n\n")
            f.write(f"Registros: {df_scaled.shape[0]:,}\n")
            f.write(f"Columnas: {df_scaled.shape[1]}\n\n")
            f.write("Método: Z-score (StandardScaler)\n")
            f.write("Variables escaladas: edad_nino, HC60, indice_riqueza, edad_madre, edu_madre, edu_madre_det\n\n")
            f.write("Estadísticas post-escalamiento:\n")
            vars_to_scale = ['edad_nino', 'HC60', 'indice_riqueza', 'edad_madre', 'edu_madre', 'edu_madre_det']
            for col in vars_to_scale:
                if col in df_scaled.columns:
                    f.write(f"  {col}: media={df_scaled[col].mean():.6f}, std={df_scaled[col].std():.6f}\n")
        
        logger.info(f"✓ Reporte guardado: {report_file}")
        logger.info(f"\n✓ FASE 5 COMPLETADA EXITOSAMENTE")
        
        return df_scaled
        
    except Exception as e:
        logger.error(f"\nError en Fase 5: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()

