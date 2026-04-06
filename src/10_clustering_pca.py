"""
10_clustering_pca.py - FASE 10: CLUSTERING + PCA + MÉTODO DEL CODO
PCA en datos ya limpios y escalados
Método del codo para determinar k óptimo
K-means clustering
Validación de clusters
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def load_scaled_data(filename="05_data_scaled.csv"):
    """Carga dataset de FASE 5 (escalado)."""
    filepath = DATA_PROCESSED / filename
    df = pd.read_csv(filepath)
    logger.info(f"Dataset cargado: {df.shape}")
    return df


def apply_pca(df):
    """Aplica PCA y analiza varianza explicada."""
    logger.info("\nAplicando PCA:")

    # Excluir HHID si existe
    features = [col for col in df.columns if col not in ['HHID', 'anemia_nivel']]
    X = df[features].dropna()

    # Aplicar PCA completo
    pca = PCA()
    pca.fit(X)

    # Varianza explicada acumulada
    cumsum_var = np.cumsum(pca.explained_variance_ratio_)

    # Encontrar número de componentes para 95% de varianza
    n_components_95 = np.argmax(cumsum_var >= 0.95) + 1

    logger.info(f"  Componentes totales: {pca.n_components_}")
    logger.info(f"  Componentes para 95% varianza: {n_components_95}")
    logger.info(f"\n  Varianza explicada por primeras 5 componentes:")
    for i in range(min(5, len(pca.explained_variance_ratio_))):
        logger.info(f"    PC{i+1}: {pca.explained_variance_ratio_[i]:.4f} ({cumsum_var[i]:.4f} acumulada)")

    # Aplicar PCA con 95% varianza
    pca_95 = PCA(n_components=n_components_95)
    X_pca = pca_95.fit_transform(X)

    logger.info(f"\n  Dataset PCA: {X_pca.shape}")

    return X_pca, pca_95


def elbow_method(X_pca):
    """Implementa método del codo para k óptimo."""
    logger.info("\nMetodo del codo:")

    inertias = []
    k_range = range(2, min(11, X_pca.shape[0]//10))

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_pca)
        inertias.append(kmeans.inertia_)
        logger.info(f"  k={k}: Inertia={kmeans.inertia_:.2f}")

    # Encontrar "codo" (cambio de pendiente)
    diffs = np.diff(inertias)
    diffs2 = np.diff(diffs)
    elbow_k = np.argmax(diffs2) + 2

    logger.info(f"\n  k optimo (codo): {elbow_k}")

    return elbow_k


def perform_kmeans(X_pca, k):
    """Realiza K-means con k óptimo."""
    logger.info(f"\nRealizando K-means con k={k}:")

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_pca)

    # Métricas de validación
    silhouette = silhouette_score(X_pca, clusters)
    davies_bouldin = davies_bouldin_score(X_pca, clusters)

    logger.info(f"  Silhouette Score: {silhouette:.4f}")
    logger.info(f"  Davies-Bouldin Index: {davies_bouldin:.4f}")

    # Distribución de clusters
    logger.info(f"\n  Distribucion de clusters:")
    unique, counts = np.unique(clusters, return_counts=True)
    for cluster, count in zip(unique, counts):
        pct = (count / len(clusters)) * 100
        logger.info(f"    Cluster {cluster}: {count:5,} ({pct:5.1f}%)")

    return kmeans, clusters


def save_clustering_results(X_pca, clusters, kmeans, k, filename="10_clustering_results.txt"):
    """Guarda resultados del clustering."""
    report_path = DATA_PROCESSED / filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("RESULTADOS CLUSTERING + PCA\n")
        f.write("="*70 + "\n\n")

        f.write("ANALISIS PCA:\n")
        f.write("-"*70 + "\n")
        f.write(f"Componentes seleccionadas: {X_pca.shape[1]}\n")
        f.write(f"Datos tras PCA: {X_pca.shape}\n\n")

        f.write("K-MEANS CLUSTERING:\n")
        f.write("-"*70 + "\n")
        f.write(f"Numero de clusters: {k}\n")
        f.write(f"Inercia: {kmeans.inertia_:.2f}\n")
        f.write(f"Silhouette Score: {silhouette_score(X_pca, clusters):.4f}\n")
        f.write(f"Davies-Bouldin Index: {davies_bouldin_score(X_pca, clusters):.4f}\n\n")

        f.write("DISTRIBUCION DE CLUSTERS:\n")
        unique, counts = np.unique(clusters, return_counts=True)
        for cluster, count in zip(unique, counts):
            pct = (count / len(clusters)) * 100
            f.write(f"  Cluster {cluster}: {count:5,} ({pct:5.1f}%)\n")

        f.write("\n" + "="*70 + "\n")
        f.write("INTERPRETACION:\n")
        f.write("="*70 + "\n")
        f.write("\nSilhouette Score: Proximidad dentro clusters vs entre clusters\n")
        f.write("  Rango: [-1, 1]\n")
        f.write("  Valores > 0.5: Buen clustering\n")
        f.write("  Valores 0.25-0.5: Moderado\n")
        f.write("  Valores < 0.25: Débil\n\n")
        f.write("Davies-Bouldin Index: Razón promedio distancia intra/inter-cluster\n")
        f.write("  Valores más bajos: Mejor separación\n")

    logger.info(f"\nResultados guardados: {report_path}")
    return report_path


def main():
    """Ejecuta FASE 10: Clustering + PCA."""
    logger.info("\n" + "="*70)
    logger.info("FASE 10: CLUSTERING + PCA + METODO DEL CODO")
    logger.info("="*70)

    df = load_scaled_data()
    X_pca, pca = apply_pca(df)
    k_optimo = elbow_method(X_pca)
    kmeans, clusters = perform_kmeans(X_pca, k_optimo)
    save_clustering_results(X_pca, clusters, kmeans, k_optimo)

    logger.info("\nFASE 10 completada\n")
    return X_pca, clusters, kmeans


if __name__ == "__main__":
    X_pca, clusters, kmeans = main()
