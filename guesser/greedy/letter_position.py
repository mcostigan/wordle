from typing import Set


class LetterPosition:
    def __init__(self, letter: str, position: int):
        self.letter = letter
        self.position = position
        self.words: Set[str] = set()

        self.is_tombstoned = False

    def add_word(self, word: str):
        self.words.add(word)

    @property
    def size(self):
        return len(self.words)

    @property
    def key(self):
        return self.letter, self.position

    def __lt__(self, other: "LetterPosition"):
        if self.is_tombstoned:
            return True
        return self.size < other.size
