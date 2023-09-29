import numpy
import numpy as np
import pandas
from sklearn.metrics import euclidean_distances
from typing import Dict, List


class NaiveKMeans(object):
    """
    All the steps of computation, including assigment history and
    centroids are saved for visualization purposes
    """

    def __init__(self, k: int,
                 ending_condition: float = 0.01,
                 max_iterations: int = 1000):
        self.k = k
        self.centroids = None
        self.assignments = None
        self.history = []
        self.rss = float('inf')
        self.ending_condition = ending_condition
        self.max_iterations = max_iterations
        ## For visualization purposes
        self.assignment_history = []
        self.centroids_history = []

    def _init_centroids(self, X: np.ndarray):
        centroids = []
        for column in range(X.shape[1]):
            values = X[:,column]
            random_values = np.random.uniform(
                values.min(), values.max(), size=self.k)
            centroids.append(random_values)
        centroids = np.array(centroids).T
        return centroids

    def compute_rss(self, clusters: Dict[int, list]):
        rss_value = 0
        for k, points in clusters.items():
            pm = np.array(points)
            c = self.centroids[k].reshape(1, -1)
            rss_value += euclidean_distances(pm, c).sum()
        return rss_value

    @staticmethod
    def clusters(X: np.ndarray,
                 assignments: np.ndarray) -> Dict[int, list]:
        clusters = dict([(i, []) for i in set(assignments)])
        for p, k in enumerate(assignments):
            clusters[k].append(X[p])
        return clusters

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
        self.assignment_history.append(self.assignments)
        self.centroids_history.append(self.centroids)
        clusters = NaiveKMeans.clusters(X, self.assignments)
        self.rss = self.compute_rss(clusters)
        self.history.append(self.rss)
        for iter in range(self.max_iterations):
            new_centroids = []
            for k, points in clusters.items():
                pm = np.array(points)
                new_centroids.append(pm.mean(axis=0))
            self.centroids = np.array(new_centroids)
            D = euclidean_distances(X, self.centroids)
            self.assignments = np.argmin(D, axis=1)
            clusters = NaiveKMeans.clusters(X, self.assignments)
            self.rss = self.compute_rss(clusters)
            if self.history[-1] - self.rss <= self.ending_condition:
                break
            else:
                self.history.append(self.rss)
                self.centroids_history.append(self.centroids)
                self.assignment_history.append(self.assignments)

    def predict(self, X: np.ndarray):
        D = euclidean_distances(X, self.centroids)
        return np.argmin(D, axis=1)










