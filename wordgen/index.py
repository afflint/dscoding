import typing as tp
import nltk
from collections import defaultdict


class WordIndex(object):
    def __init__(self, corpus: tp.List[str]):
        self.corpus = corpus
        self.index = defaultdict(lambda: 0)
        self.read()

    def read(self):
        for document in self.corpus:
            for word in nltk.word_tokenize(document):
                self.index[word] += 1


