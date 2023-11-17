import numpy as np
from sklearn.preprocessing import MinMaxScaler


class KMeans:
    def __init__(self, k: int):
        self.k = k
        self.centroids = None
        self.assignment = None
        self.current_rss = float('inf')

    def _init_centroids(self, X: np.ndarray):
        c = []
        for i in range(X.shape[1]):
            col = X[:,i]
            c_i = np.random.uniform(low=col.min(), high=col.max(), size=self.k)
            c.append(c_i)
        self.centroids = np.array(c).T

    def _assigment(self, Xs: np.ndarray):
        for i, point in enumerate(Xs):
            delta = np.array([np.linalg.norm(point - c) for c in self.centroids])
            self.assignment[i] = np.argmin(delta)

    def fit(self, X: np.ndarray):
        scaler = MinMaxScaler()
        Xs = scaler.fit_transform(X)
        self._init_centroids(Xs)
        self.assignment = np.zeros(Xs.shape[0])
        self._assigment(Xs)
        # refine the centroids
        for i, c in enumerate(self.centroids):
            point_indexes = [j for j, x in enumerate(self.assignment) if x == i]
            cluster = Xs[point_indexes, :]
            self.centroids[i] = cluster.mean(axis=0)
        return Xs


