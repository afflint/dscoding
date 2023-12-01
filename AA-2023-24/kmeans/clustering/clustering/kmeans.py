import numpy as np
from sklearn.preprocessing import MinMaxScaler


class KMeans:
    def __init__(self, k: int):
        self.k = k
        self.centroids = None
        self.assignment = None
        self.current_rss = float('inf')
        self.rss_history = []

    def _init_centroids(self, X: np.ndarray):
        c = []
        for i in range(X.shape[1]):
            col = X[:,i]
            c_i = np.random.uniform(size=self.k)
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
        for iter in range(10000):
            print('run iter {} : rss {}'.format(iter, self.rss(Xs)))
            self._assigment(Xs)
            # refine the centroids
            for i, c in enumerate(self.centroids):
                point_indexes = [j for j, x in enumerate(self.assignment) if x == i]
                cluster = Xs[point_indexes, :]
                if cluster.shape[0] == 0:
                    pass
                else:
                    self.centroids[i] = cluster.mean(axis=0)
            r = self.rss(Xs)
            if len(self.rss_history) > 0 and r - self.rss_history[-1] < 0.01:
                break
            else:
                self.rss_history.append(r)
        return Xs

    def rss(self, Xs: np.ndarray):
        rss = 0
        for i, c in enumerate(self.centroids):
            point_indexes = [j for j, x in enumerate(self.assignment) if x == i]
            cluster = Xs[point_indexes, :]
            for point in cluster:
                delta = np.linalg.norm(point - c)
                rss += delta**2
        return rss





