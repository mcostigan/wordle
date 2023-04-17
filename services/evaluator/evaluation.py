from dataclasses import dataclass
from typing import List, Type

from models.wordle_guesser import WordleGuesser


@dataclass
class Guess:
    guess: str
    possibilities: int


class Game:
    def __init__(self, target: str):
        self.target = target
        self.guesses: List[Guess] = []

    def add_guess(self, guess: Guess):
        self.guesses.append(guess)

    def number_of_guesses(self) -> int:
        return len(self.guesses)

    def is_won(self):
        return len(self.guesses) < 7


class Evaluation:
    def __init__(self, guesser: Type[WordleGuesser]):
        self.guesser: Type[WordleGuesser] = guesser
        self.games: List[Game] = []
        self._games_won = 0
        self._total_guesses = 0

    def add_game(self, game: Game):
        self._total_guesses += game.number_of_guesses()
        self._games_won += 1 if game.is_won() else 0
        self.games.append(game)

    @property
    def guesser_name(self):
        return self.guesser.__name__

    @property
    def avg(self) -> float:
        return self._total_guesses / len(self.games)

    @property
    def win_pct(self):
        return self._games_won / len(self.games)

    def __str__(self):
        return f"guesser: {self.guesser.__name__}, avg: {self.avg}, win_pct: {self.win_pct}"
