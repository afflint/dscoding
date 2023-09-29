import typing as tp
import nltk
from collections import defaultdict
from abc import ABC, abstractmethod


class WordIndex(object):
    def __init__(self, corpus: tp.List[str]):
        self.corpus = corpus
        self.index = defaultdict(lambda: 0)
        self.read()

    def read(self):
        for document in self.corpus:
            for word in nltk.word_tokenize(document):
                self.index[word] += 1


class CharIndex(ABC):

    @abstractmethod
    def index_word(self, word: str,
                   frequency: int = 1, lower_case: bool = False):
        pass


class UnigramIndex(CharIndex):
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


class BiGramIndex(CharIndex):

    def __init__(self):
        self.index = defaultdict(lambda : defaultdict(lambda : 0))

    def index_word(self, word: str, frequency: int = 1, lower_case: bool = False):
        for (a, b) in nltk.ngrams(word, n=2):
            self.index[a][b] += frequency
        self.index[word[-1]][' '] += frequency

    def __getitem__(self, item: tp.Tuple[str,str]):
        return self.index[item[0]][item[1]]

    def frequency(self, char: str):
        return sum(self.index[char].values())

    @staticmethod
    def from_word_index(word_index: WordIndex,
                        lower_case: bool = False):
        i = BiGramIndex()
        for word, frequency in word_index.index.items():
            i.index_word(word, frequency=frequency, lower_case=lower_case)
        return i



