import string
from typing import List, Dict

from guesser.greedy.letter_position import LetterPosition
from models.constraint import Constraint
from models.wordle_guesser import WordleGuesser
from services.constraint_service import ConstraintService


class GreedyGuesser(WordleGuesser):
    """
    Starts by guessing the most common letter-position combination, `x`. Then, it guesses the next most common letter-position,`y` given that it shares a word with the `x`.
    This continues until a 5-letter word is created. 
    """

    def __init__(self, candidates: List[str]):

        super().__init__(candidates)
        self.candidates = candidates
        self._tombstones = set()
        self._letter_position_index: Dict[tuple, LetterPosition] = {(char, i): LetterPosition(char, i) for i in range(5)
                                                                    for char in
                                                                    string.ascii_lowercase}
        self._letter_positions = self._build_nodes(candidates)

    def _build_nodes(self, words: List[str]):
        def add_letter_positions(new_word: str):
            for i in range(5):
                node: LetterPosition = self._letter_position_index[(new_word[i], i)]
                node.add_word(new_word)

        for word in words:
            if word in self._tombstones:
                continue
            add_letter_positions(word)
        return sorted(self._letter_position_index.values(), reverse=True)

    def guess_word(self) -> str:
        selected_letters = []
        i = 0
        eligible_words = set(self.candidates).difference(self._tombstones)
        while len(selected_letters) < 5:
            letter_position = self._letter_positions[i]
            intersection = letter_position.words.intersection(eligible_words)
            if intersection:
                selected_letters.append(letter_position)
                eligible_words = intersection

            i += 1

        return ''.join(
            [letter_position.letter for letter_position in sorted(selected_letters, key=lambda x: x.position)])

    def receive_feedback(self, constraints: List[Constraint], guess: str):
        for word in self.candidates:
            if word in self._tombstones:
                continue
            if ConstraintService.are_violated(constraints=constraints, word=word):
                self._tombstones.add(word)

        self._letter_positions = self._build_nodes(self.candidates)

    def solution_space(self) -> int:
        return len(self.candidates) - len(self._tombstones)

    def reset(self):
        self._tombstones = set()
