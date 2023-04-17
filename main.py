from guesser.expected_value_guesser.guesser import ExpectedValueGuesser
from guesser.greedy.guesser import GreedyGuesser
from guesser.left_to_right.guesser import LeftToRightGuesser
from services.candidate_service import CandidateService
from services.evaluator.evaluation_service import EvaluationService

if __name__ == '__main__':
    candidates = CandidateService.get_candidates()
    evaluator = EvaluationService([ExpectedValueGuesser, GreedyGuesser, LeftToRightGuesser], candidates, sample_size=50)
    evaluator.evaluate()
