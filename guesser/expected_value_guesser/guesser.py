import string
from typing import List, Tuple, Dict

from models.constraint import Constraint
from models.wordle_guesser import WordleGuesser
from services.constraint_service import ConstraintService


class ExpectedValueGuesser(WordleGuesser):
    """
    Given a value assigned to `GREEN` and `YELLOW` and a list of candidate words, guesses the word with the highest expected value. 
    """

    def __init__(self, candidates: List[str]):
        super().__init__(candidates)
        self._candidates = candidates
        self._tombstones = set()
        self._letter_position_counts, self._letter_counts = self._build_histograms()

    def _build_histograms(self) -> Tuple[Dict[Tuple[str, int], int], Dict[str, int]]:
        letter_position_histogram = {(letter, position): 0 for position in range(5) for letter in
                                     string.ascii_lowercase}
        letter_histogram = {letter: 0 for letter in string.ascii_lowercase}
        for word in self._candidates:
            if word in self._tombstones:
                continue
            seen = set()
            for position, letter in enumerate(word):
                if letter not in seen:
                    letter_histogram[letter] += 1
                    seen.add(letter)
                key = (letter, position)
                letter_position_histogram[key] += 1
        return letter_position_histogram, letter_histogram

    def guess_word(self) -> str:
        def get_expected_value(word: str) -> int:
            """

            :param word: 
            :return: 
            """
            ev = 0
            for position, letter in enumerate(word):
                greens = self._letter_position_counts[(letter, position)] / self.size
                yellows = self._letter_counts[letter] / self.size - greens
                grays = 1 - greens - yellows
                ev += greens + (yellows * .25)
            return ev

        best_guess = (-1, '')
        for word in self._candidates:
            if word in self._tombstones:
                continue
            best_guess = max((get_expected_value(word), word), best_guess)
        return best_guess[1]

    def solution_space(self) -> int:
        return self.size

    def receive_feedback(self, constraints: List[Constraint], guess: str):
        for word in self._candidates:
            if word in self._tombstones:
                continue
            if ConstraintService.are_violated(constraints=constraints, word=word):
                self._tombstones.add(word)
        self._letter_position_counts, self._letter_counts = self._build_histograms()

    @property
    def size(self):
        return len(self._candidates) - len(self._tombstones)

    def reset(self):
        self._tombstones = set()
