import random
import threading
from typing import List, Optional, Type

from models.wordle_guesser import WordleGuesser
from services.constraint_service import ConstraintService
from services.evaluator.evaluation import Evaluation, Game, Guess
from services.mpl.mpl_service import MplService


class EvaluationService:
    """
    Evaluates the efficacy of one or more `WordleGuesser`s. 
    
    Given an array of `WordleGuesser` types, it instantiates each type, and runs it on a sample of size `sample_size`. The average number of guesses, win percentage, and a histogram of guess counts are displayed.
    """

    def __init__(self, guesser_types: List[Type[WordleGuesser]], candidates: List[str],
                 sample_size: Optional[int] = None):
        self.guessers = [guesser_type(candidates=candidates) for guesser_type in guesser_types]
        self.candidates = candidates
        self.sample_size = sample_size if sample_size else len(candidates)

    def evaluate(self):
        evaluations = self._evaluate_guessers()
        for evaluation in evaluations:
            print(evaluation)
            MplService.histogram(evaluation.guesser_name, evaluation, x_label="# of guesses")

    def _evaluate_guessers(self) -> List[Evaluation]:
        def threaded_evaluator(guesser: WordleGuesser, sample_words: List[str], results: List[Evaluation]):
            results.append(self._evaluate_guesser(guesser, sample_words))

        sample_words = random.sample(self.candidates, self.sample_size)
        results = []
        threads = []
        for guesser in self.guessers:
            thread = threading.Thread(target=threaded_evaluator, args=(guesser, sample_words, results))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return results

    def _evaluate_guesser(self, guesser: WordleGuesser, sample_words: List[str]) -> Evaluation:
        evaluation = Evaluation(guesser.__class__)
        for sample_word in sample_words:
            game = self._play_game(guesser, sample_word)
            evaluation.add_game(game)
            guesser.reset()
        return evaluation

    def _play_game(self, guesser: WordleGuesser, solution: str) -> Game:
        game = Game(solution)

        guess_word = ''
        while solution != guess_word:
            guess_word = guesser.guess_word()

            guess = Guess(guess_word, guesser.solution_space())
            game.add_guess(guess)

            constraints = ConstraintService.get_constraints_from_solution(guess=guess_word, solution=solution)
            guesser.receive_feedback(constraints, guess_word)

        return game
