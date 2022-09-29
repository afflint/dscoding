import numpy as np
from typing import List


class DummyWordGenerator(object):
    """
    A naive word generation model that just selects random chars
    from a vocabulary
    """
    def __init__(self,
                 alphabet: str,
                 special_chars: str,
                 max_len: int = 1000,
                 p: List[int] = None
                 ):
        """
        Dummy generator of words
        :param alphabet: the alphabet from which sampling letters
        :param special_chars: set of special chars that stops the generation process
        :param max_len: of words if stop char is not extracted
        :param p: parameters for generating the distribution of probabilities of chars
        """
        self.max_len = max_len
        self.alphabet = list(alphabet + special_chars)
        self.special_chars = set(special_chars)
        if p is None:
            self.p = np.ones(len(self.alphabet)) / len(self.alphabet)
        else:
            self.p = np.array(p) / sum(p)

    @property
    def generate(self) -> List[str]:
        output = []
        for it in range(self.max_len):
            k = np.random.choice(self.alphabet, p=self.p)
            if k in self.special_chars:
                break
            else:
                output.append(k)
        return output

    def words(self, size: int):
        for i in range(size):
            yield "".join(self.generate)

