"""
This file contains the GrammarTree class, which is a recursive tree data structure
that represents a constituent parse tree of an English sentence.

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""


class GrammarTree:
    """
    A recursive tree data structure that represents a constituent parse tree of an
    English sentence.

    Representation Invariants:
        - (self._subtrees == []) == (self._root["text"] != "")
        - self._root["text"] == "" or self._root["text"] is an English word or valid punctuation.
    """
    # Private Instance Attributes:
    #   - _root:
    #       Stores the constituent tag (e.g. "S", "NP", "VP", "NN", etc.) of the tree
    #       in _root["label"] and, if the tree represents a word, stores what the word
    #       is in _root["text"] (otherwise _root["text"] is just an empty string).
    #   - _subtrees:
    #       Stores a list of GrammarTree objects that represent children of the
    #       constituent parse tree this GrammarTree is representing. _subtrees is
    #       empty means this GrammarTree represents a constituent parse tree of a word.

    _root: dict[str: str]
    _subtrees: list["GrammarTree"]

    def __init__(self, label: str, subtrees: list["GrammarTree"], text: str = "") -> None:
        self._root = {"label": label, "text": text}
        self._subtrees = subtrees

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self._root == []:
            return ''
        else:
            if len(self._root["text"]) > 0:
                s = '  ' * depth + f'{self._root["label"]}: {self._root["text"]}\n'
            else:
                s = '  ' * depth + f'{self._root["label"]}\n'
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def get_root(self) -> dict[str: str]:
        """Return the _root value of the tree."""
        return self._root

    def get_subtrees(self) -> list["GrammarTree"]:
        """Return the _subtrees value of the tree."""
        return self._subtrees

    def find_the_last(self) -> str:
        """Return the end punctuation of the sentence represented by the tree, if
        the sentence has an end punctuation. Otherwise, the returned string is
        the _root['text'] value of the last subtree of this tree.

        Example usages see test_find_the_last() in tests_GrammarTree_methods.py.
        """
        s = self
        last = s._subtrees[-1]
        return last._root['text']

    def contain_type(self, kind: str) -> bool:
        """Return whether the entire tree contains the input type of constituent tag.

        Example usages see test_contain_type() in tests_GrammarTree_methods.py.
        """
        if self._root['label'] == kind:
            return True
        else:
            return any(i.contain_type(kind) for i in self._subtrees)

    def contain_content(self, word_or_punc: str) -> bool:
        """Return whether the entire tree contains the input word/punctuation mark.

        Example usages see test_contain_content() in tests_GrammarTree_methods.py.
        """
        if self._root['text'] == word_or_punc:
            return True
        else:
            return any(i.contain_content(word_or_punc) for i in self._subtrees)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['_grammar_checking_methods1', '_grammar_checking_methods2', 'typing'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
