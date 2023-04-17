import matplotlib.pyplot as plt

from services.evaluator.evaluation import Evaluation


class MplService:

    @classmethod
    def histogram(cls, title: str, evaluation_result: Evaluation, x_label: str = 'keys', y_label: str = 'frequency'):
        collapsed = {}
        data = evaluation_result.games
        for item in data:
            collapsed[item.number_of_guesses()] = collapsed.get(item.number_of_guesses(), 0) + 1

        plt.bar(collapsed.keys(), [value / len(data) for value in collapsed.values()])
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
