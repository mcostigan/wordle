from typing import List

from models.constraint import Constraint
from models.trie import Trie, TrieNode
from services.constraint_service import ConstraintService


class WordleTrieNode(TrieNode):
    def get_biggest_child(self) -> "WordleTrieNode":
        return max(self.children)


class WordleTrie(Trie[WordleTrieNode]):

    def greedy_word(self):
        node: WordleTrieNode = self.root
        path = []
        while not node.is_leaf:
            node = node.get_biggest_child()
            path.append(node)

        return ''.join([node.character for node in path])

    def constrain(self, constraints: List[Constraint]):
        def node_violates_constraint(node: TrieNode):
            return ConstraintService.are_violated(constraints=constraints, character=node.character,
                                                  position=node.position, word=node.word)

        def should_continue_function(node: TrieNode):
            constraint_violated = node_violates_constraint(node)

            if constraint_violated:
                node.tombstone()
                return False

            return True

        self.walk(should_continue_function)

    def build_node(self, character: str, position: int) -> WordleTrieNode:
        return WordleTrieNode(character, position)


if __name__ == '__main__':
    trie = WordleTrie()
    trie.add_words(["arm", "army", "art", "bear"])
    print(trie.greedy_word())
