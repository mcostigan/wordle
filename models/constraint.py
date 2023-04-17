from dataclasses import dataclass
from enum import Enum
from typing import Set, List, Tuple


class ConstraintType(Enum):
    LETTER_AT = "letter at"
    LETTER_NOT_AT = "letter not at"
    SUBSET_CONTAINS = "subset contains"


@dataclass
class Constraint:
    type: ConstraintType
    character: str
    positions: Tuple[int]

    def __hash__(self):
        return hash((self.type, self.character, self.positions))

    def __eq__(self, other: "Constraint"):
        return self.type == other.type and self.character == other.character and self.positions == other.positions

    def is_violated(self, character: str, position: int, word):
        if self.type == ConstraintType.LETTER_AT:
            return position in self.positions and character != self.character
        elif self.type == ConstraintType.LETTER_NOT_AT:
            return position in self.positions and character == self.character
        elif self.type == ConstraintType.SUBSET_CONTAINS:
            if word == '':
                return False
            return all(self.character != word[position] for position in self.positions)


class Constraints:
    def __init__(self):
        # set of unique constraints applicable to the current game
        self._constraints: Set[Constraint] = set()

    def are_violated(self, character: str = '', position: int = -1, word: str = ''):
        pass

    def add_from_colors(self, guess: str, colors: List[str]):
        pass

    def reset(self):
        self._constraints = set()
