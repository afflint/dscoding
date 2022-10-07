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


class UnigramIndex(object):
    """
    Provides unigram probability estimation
    (eventually) given a word index
    """
    def __init__(self):
        self.index = defaultdict(lambda: 0)

    def index_word(self, word: str, frequency: int = 1,
                   lower_case: bool = False):
        if lower_case:
            w = word.lower()
        else:
            w = word
        for c in w:
            self.index[c] += frequency
        self.index[' '] += frequency

    def __getitem__(self, char: str):
        return self.index[char]

    @staticmethod
    def from_word_index(word_index: WordIndex,
                        lower_case: bool = False):
        """
        A static method that provides and initialization mechanism
        for UnigramIndex
        :param word_index: the word index
        :param lower_case: check if lowercase (default false)
        :return: an instance of UnigramIndex
        """
        i = UnigramIndex()
        for word, frequency in word_index.index.items():
            i.index_word(word, frequency=frequency, lower_case=lower_case)
        return i




