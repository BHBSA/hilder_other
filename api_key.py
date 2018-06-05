import re

import reprlib


class SentenceIterator:
    def __init__(self):
        self.words = ['a', 'b']
        self.index = 0


def __next__(self):
    try:
        word = self.words[self.index]
    except IndexError:
        raise StopIteration()
    self.index += 1
    return word


if __name__ == '__main__':
    s = SentenceIterator()
    print(s.index)
    print(s.index)