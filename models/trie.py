from typing import List, Dict, TypeVar, Generic, Optional, Callable


class TrieNode:
    parent: Optional["TrieNode"]
    _children: Dict[str, "TrieNode"]

    character: str
    position: int

    size: int
    is_tombstoned: bool

    word: str

    def __init__(self, character: str, position: int, parent: Optional["TrieNode"] = None):
        self.character = character
        self.position = position
        self.parent = parent

        self._children = {}
        self.size = 0
        self.is_tombstoned = False

        self.word = ''

    def has_child(self, character: str) -> bool:
        return character in self._children

    def get_or_create_child(self, character: str) -> "TrieNode":
        child = self._children.get(character, self.__class__(character, self.position + 1, self))
        self._children[character] = child
        return child

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def children(self) -> List["TrieNode"]:
        return [child for child in self._children.values() if not child.is_tombstoned]

    def __lt__(self, other: "TrieNode"):
        if self.is_tombstoned:
            return True
        return self.size < other.size

    def tombstone(self):
        self.is_tombstoned = True
        self.size = 0

        # repair up
        node = self.parent
        while node:
            node.size = sum([child.size for child in node._children.values()])
            if node.size == 0:
                node.is_tombstoned = True
            node = node.parent

    def untombstone(self):
        self.is_tombstoned = False
        if self.word != '':
            self.size = 1
            return

        for child in self._children.values():
            child.untombstone()

        self.size = sum([child.size for child in self.children])

    def walk(self, should_continue_func: Callable[["TrieNode"], bool]):
        should_continue = should_continue_func(self)

        if should_continue:
            for child in self.children:
                child.walk(should_continue_func)


T = TypeVar('T')


class Trie(Generic[T]):
    root: T

    def build_node(self, character: str, position: int) -> T:
        return TrieNode(character, position)

    def __init__(self):
        self.root = self.build_node('', -1)

    def add_word(self, word: str):
        node = self.root
        self.root.size += 1

        for position, character in enumerate(word):
            node = node.get_or_create_child(character)
            node.size += 1

        node.word = word

    @property
    def size(self) -> int:
        return self.root.size

    def add_words(self, words: List[str]):
        for word in words:
            self.add_word(word)

    def walk(self, should_continue_func: Callable[[TrieNode], bool]):
        def noop_should_continue_func(node: TrieNode) -> bool:
            return True

        self.root.walk(should_continue_func if should_continue_func else noop_should_continue_func)
