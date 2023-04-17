from abc import ABC
from typing import List

from models.constraint import Constraint


class WordleGuesser(ABC):
    def __init__(self, candidates: List[str]):
        pass

    def _add_candidates(self, candidates: List[str]):
        """
        informs the guesser of all possible solutions
        :param candidates: list of string solutions
        :return: None
        """
        pass

    def receive_feedback(self, constraints: List[Constraint], guess: str):
        """
        limits the possible solutions given a list of constraints
        :param guess: 
        :param constraints: a list of Constraint objects
        :return: None
        """
        pass

    def guess_word(self) -> str:
        """
        
        :return: the guesser's best guess given all remainding candidate words
        """
        pass

    def solution_space(self) -> int:
        """
        
        :return: The number of words that could possibly be a solution to the game
        """
        pass

    def reset(self):
        """
        restores the guesser and all of its candidates to their starting position
        :return: 
        """
        pass
