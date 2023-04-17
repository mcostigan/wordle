from collections import defaultdict
from typing import List, Dict, Set, Iterable

from models.constraint import Constraint, ConstraintType


class ConstraintService:
    @classmethod
    def get_colors_from_string(cls, guess: str, result: str) -> List[str]:
        colors = result.split(",")
        return colors

    @classmethod
    def get_colors_from_solution(cls, guess: str, solution: str) -> List[str]:
        def string_to_dict(s: str) -> Dict[str, Set[int]]:
            d = {}
            for position, character in enumerate(s):
                character_set = d.get(character, set())
                character_set.add(position)
                d[character] = character_set
            return d

        def find_greens(colors: List[str], guess_dict: Dict[str, Set[int]], solution_dict: Dict[str, Set[int]]):
            """

            Loop through every guessed character and check if there is an intersection between the positions in which it was guessed
            and any positions in the solution.

            If a position is matched, then remove the position from both maps.

            :param colors: result array to update with 'greens'
            :param guess_dict: a map of guessed characters to positions
            :param solution_dict: a map of solution characters to positions
            :return: None
            """
            for guess_key in guess_dict:
                guess_positions = guess_dict[guess_key]
                solution_positions = solution_dict.get(guess_key, set())

                green_positions = guess_positions.intersection(solution_positions)
                for position in green_positions:
                    colors[position] = 'green'
                    solution_positions.remove(position)
                    guess_positions.remove(position)

        def find_yellows(colors: List[str], guess_dict: Dict[str, Set[int]], solution_dict: Dict[str, Set[int]]):
            """

            Looks for keys that exist in both dicts. If, for a given key, a position set has `m` positions in the `guess_dict` and `n` positions in the `solutions_dict`
            then `n` positions from `guess_positions` are assigned yellow. `m-n` positions will be left gray

            :param colors: result array to update with 'yellows'
            :param guess_dict: a map of guessed characters to positions
            :param solution_dict: a map of solution characters to positions
            :return: None
            """
            for guess_key in guess_dict:
                guess_set = guess_dict[guess_key]
                solution_set = solution_dict.get(guess_key, set())
                no_of_yellows = range(min(len(solution_set), len(guess_set)))
                for _ in no_of_yellows:
                    yellow_position = guess_set.pop()
                    colors[yellow_position] = 'yellow'

        guess_dict = string_to_dict(guess)
        solution_dict = string_to_dict(solution)
        colors = ['gray'] * 5
        find_greens(colors, guess_dict, solution_dict)
        find_yellows(colors, guess_dict, solution_dict)

        return colors

    @classmethod
    def _get_constraints_from_colors(cls, colors: List[str], guess: str) -> List[Constraint]:
        def default_positions():
            return set(range(5))

        constraints: Set[Constraint] = set()

        # process the most restrictive constraints first
        prioritized_colors = sorted(
            [(colors[position], character, position) for position, character in enumerate(guess)],
            key=lambda x: 0 if x[0] == 'green' else 1 if x[0] == 'yellow' else 2)

        available_positions_by_letter: Dict[str, Set[int]] = defaultdict(default_positions)

        for color, character, position in prioritized_colors:
            # find all positions not categorized by prior constraints
            available_positions: Set[int] = available_positions_by_letter[character]

            # if green, any future word MUST have `character` at `position`
            if color == 'green':
                constraints.add((Constraint(ConstraintType.LETTER_AT, character, (position,))))
                # position is spoken for
                available_positions.discard(position)
            elif color == 'yellow':
                constraints.add((Constraint(ConstraintType.LETTER_NOT_AT, character, (position,))))
                available_positions.discard(position)

                if available_positions:
                    # if yellow, then letter is not at current_position but is in at least one of its available positions
                    constraints.add(
                        Constraint(ConstraintType.SUBSET_CONTAINS, character, tuple(available_positions)))
                    # all available positions are now expressed in the SUBSET_CONTAINS constraint
                    available_positions.clear()
            elif color == 'gray':
                # if gray, then letter is definitely not at any of its current non-green positions
                constraints.add(Constraint(ConstraintType.LETTER_NOT_AT, character, tuple(available_positions)))
                # all available positions are now expressed in the SUBSET_CONTAINS constraint
                available_positions.clear()
            else:
                raise "Bad Color !"
            # update the available position based on changes
            available_positions_by_letter[character] = available_positions

        return list(constraints)

    @classmethod
    def are_violated(cls, constraints: Iterable[Constraint], character: str = '', position: int = -1,
                     word: str = '') -> bool:
        """
        Give either a letter and its position OR a word, checks if any of the provided constraints are violated

        :param constraints: Collection of constraints
        :param character: current letter
        :param position: current position
        :param word: current word
        :return: `True` if any constraint has been violated. Else, `False`.
        """
        if word != '':
            return any([any(constraint.is_violated(character, position, word) for constraint in constraints) for
                        position, character in enumerate(word)])
        return any([constraint.is_violated(character, position, word) for constraint in constraints])

    @classmethod
    def get_constraints_from_solution(cls, solution: str, guess: str) -> List[Constraint]:
        colors = cls.get_colors_from_solution(solution=solution, guess=guess)
        return cls._get_constraints_from_colors(colors=colors, guess=guess)
