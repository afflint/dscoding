import numpy
import numpy as np
import pandas
from sklearn.metrics import euclidean_distances


class NaiveKMeans(object):

    def __init__(self, k: int,
                 ending_condition: float = 0.01):
        self.k = k
        self.centroids = None
        self.assignments = None
        self.history = []
        self.rss = float('inf')

    def _init_centroids(self, X: np.ndarray):
        centroids = []
        for column in range(X.shape[1]):
            values = X[:,column]
            random_values = np.random.uniform(
                values.min(), values.max(), size=self.k)
            centroids.append(random_values)
        centroids = np.array(centroids).T
        return centroids

    def fit(self, X: np.ndarray):
        """
        Fits the algorithms parameters
        Steps:
        - init centroids and assignment
        - performs iterations until ending
            - compute distances between data and centroids
            - assign points to centroids
            - compute RSS
            - check ending condition
            - compute new centroids
        :param data: matrix of points sample \times features
        :return: None
        """
        self.centroids = self._init_centroids(X)
        D = euclidean_distances(X, self.centroids)
        self.assignments = np.argmin(D, axis=1)






