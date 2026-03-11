from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def cluster_operating_states(proxy_df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    """Cluster operating states and return labels with medoid flags."""
    feature_cols = ["v_dep", "v_imb", "u_inc", "c_inc", "load_ramp", "ramp_dispersion", "k_stiff"]
    X = proxy_df[feature_cols].to_numpy()
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    labels = model.fit_predict(Xs)
    centers = model.cluster_centers_

    out = proxy_df.copy()
    out["cluster"] = labels
    out["is_medoid"] = False

    for k in range(n_clusters):
        idx = np.where(labels == k)[0]
        if idx.size == 0:
            continue
        cluster_points = Xs[idx]
        d = ((cluster_points - centers[k]) ** 2).sum(axis=1)
        medoid_local = int(np.argmin(d))
        out.loc[out.index[idx[medoid_local]], "is_medoid"] = True

    return out
