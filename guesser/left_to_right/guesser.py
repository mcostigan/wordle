from typing import List

from guesser.left_to_right.wordle_trie import WordleTrie
from models.constraint import Constraint
from models.wordle_guesser import WordleGuesser


class LeftToRightGuesser(WordleGuesser):
    """
    Given candidate words, guesses the most common first letter. And given the most common first letter, guesses the most common second letter.
    This continues until a 5-letter word is created.
    """

    def __init__(self, candidates: List[str]):
        super().__init__(candidates)
        self._trie = WordleTrie()
        self._add_candidates(candidates)
        self._latest_guess: str = ''

    def _add_candidates(self, candidates: List[str]):
        self._trie.add_words(candidates)

    def receive_feedback(self, constraints: List[Constraint], guess: str):
        self._trie.constrain(constraints)

    def guess_word(self) -> str:
        return self._trie.greedy_word()

    def solution_space(self) -> int:
        return self._trie.size

    def reset(self):
        self._trie.root.untombstone()
