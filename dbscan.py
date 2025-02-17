from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns


def norm(tab):
    ma = np.array(
        [
            max(abs(max(e)), abs(min(e))) if max(abs(max(e)), abs(min(e))) != 0 else 1
            for e in tab.transpose()
        ]
    )
    return tab / ma


n = 100


ft = norm(
    np.concatenate(
        list((np.loadtxt(f"data/f{i}.csv") for i in range(1, 4))),
        axis=0,
    )
)


print(ft.shape)


to_hist = metrics.euclidean_distances(ft).ravel()
plt.hist(to_hist, bins=50)
plt.show()
print(np.median(to_hist))
print(to_hist.std())


db = DBSCAN(eps=5.3).fit(ft)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_


n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print(f"Estimated number of clusters: {n_clusters_}")
print(f"Estimated number of noise points: {n_noise_}")
clusters = [np.arange(ft.shape[0])[labels == i] for i in set(list(labels)) - {-1}]
data = norm(
    np.concatenate(
        list(
            (
                np.array(pd.read_csv(f"data/data{i}.csv"))[:, 1:]
                for i in range(1, 7)
            )
        ),
        axis=0,
    )
)


x = np.arange(data.shape[1])
for i, cluster in enumerate(clusters):
    print(f"Generating cluster {i}: {len(cluster)} graphs")
    graph = sns.JointGrid(x, x)
    prec = 0
    end = len(cluster)
    for j, y in enumerate(data[list(cluster)]):
        if int(100*j/end) != prec:
            prec = int(100*j/end)
            if prec < 10:
                print(f"0{prec}%")
            else:
                print(f"{prec}%")
        graph.y = y
        graph.plot_joint(plt.scatter, marker="+")
        graph.plot_marginals(sns.distplot)
    plt.title(f"Cluster {i}")
    plt.show()
