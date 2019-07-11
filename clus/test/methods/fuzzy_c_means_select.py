import os

import numpy as np
from scipy.cluster.hierarchy import fcluster
from scipy.spatial.distance import cdist
from scipy.cluster.hierarchy import linkage

import pandas as pd

from sklearn.datasets import load_iris

from clus import fuzzy_c_means
from clus.src.core.methods import fuzzy_c_means_select
from clus.src.core.visualisation import plot_dendrogram, visualise_clustering_2d, visualise_clustering_3d
from clus.src.utils.random import set_manual_seed
from clus.src.core.normalization import normalization as normalize


PATH_DIR_DATA = r"D:\work\projects\_data\processed"
# PATH_DIR_DATA = r"/local/bizzozzero/data/hyperstars/processed/n02_pw05_vs07"

PATH_DIR_RESULTS = r"D:\work\projects\_data\processed"
# PATH_DIR_RESULTS = r"/local/bizzozzero/results/clustering"


def test(seed):
    set_manual_seed(seed)

    components = 500
    eps = 1e-4
    max_iter = 200
    fuzzifier = 2.0
    batch_size = 10000
    max_epochs = 2
    min_centroid_size = 10
    max_centroid_diameter = 10000000.0
    normalization = "rescaling"
    weights = [1, 1, 1, 0]

    data = pd.read_csv(os.path.join(PATH_DIR_DATA, "rhocut-filtered-1e02.csv"),
                       header=0).values
    data = data.astype(np.float64)
    normalize(data, strategy=normalization)
    data = data * np.sqrt(weights)

    clus_results = \
        fuzzy_c_means_select(data, components=components, eps=eps, max_iter=max_iter, fuzzifier=fuzzifier,
                             batch_size=batch_size, weights=None, max_epochs=max_epochs,
                             min_centroid_size=min_centroid_size, max_centroid_diameter=max_centroid_diameter,
                             initialization_method="random_choice",
                             empty_clusters_method="nothing", centroids=None, progress_bar=False)

    flat_clusters = fcluster(clus_results["linkage_mtx"], criterion="maxclust", t=31)

    _plot_clus_rhocut(data=data[clus_results["good_data_idx"]], affectations=flat_clusters)


def test_fcm(seed):
    set_manual_seed(seed)

    path_data = os.path.join(PATH_DIR_RESULTS,
                             'rhocut-filtered-1e02_fcm_10000_2.0_001_weighted-euclidean-(001-001-001-000).npz')
    clusters_center = np.load(path_data)["clusters_center"]

    flat_clusters = fcluster(linkage(clusters_center, method="single"), criterion="maxclust", t=31)

    _plot_clus_rhocut(data=clusters_center, affectations=flat_clusters)


def _plot_clus_rhocut(data, affectations):
    print("DATA")
    print("data  :", data)
    print("shape :", data.shape)
    print("min   :", data.min(0))
    print("max   :", data.max(0))
    print("mean  :", data.mean(0))
    print("std   :", data.std(0))

    print("AFFECTATIONS")
    print("data  :", affectations)
    print("shape :", affectations.shape)
    print("min   :", affectations.min(0))
    print("max   :", affectations.max(0))
    print("mean  :", affectations.mean(0))
    print("std   :", affectations.std(0))

    data_visu = np.zeros_like(data[:, :3])

    # Swap columns for 3D visualisation
    tmp_x = np.copy(data[:, 0])
    tmp_y = np.copy(data[:, 1])
    tmp_z = np.copy(data[:, 2])
    data_visu[:, 0] = tmp_z
    data_visu[:, 1] = tmp_x
    data_visu[:, 2] = tmp_y

    visualise_clustering_3d(data_visu, clusters_center=None, affectations=affectations,
                            clustering_method="fcm-select",
                            dataset_name="iris", header=None,
                            show=True, save=False, saving_path=None)


if __name__ == "__main__":
    test(seed=1)
    test_fcm(seed=1)
