"""
This file contains the GrammarTree class, which is a recursive tree data structure
that represents a constituent parse tree of an English sentence.

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""


class GrammarTree:
    """
    A recursive tree data structure that represents a constituent parse tree of an
    English sentence.
    Instance Attributes:
        - root:
            Stores the constituent tag (e.g. "S", "NP", "VP", "NN", etc.) of the tree
            in root["label"] and, if the tree represents a word, stores what the word
            is in root["text"] (otherwise root["text"] is just an empty string).
        - subtrees:
            Stores a list of GrammarTree objects that represent children of the
            constituent parse tree this GrammarTree is representing. subtrees is
            empty means this GrammarTree represents a constituent parse tree of a word.
    Representation Invariants:
        - (self.subtrees == []) == (self.root["text"] != "")
    """
    root: dict[str: str]
    subtrees: list["GrammarTree"]

    def __init__(self, label: str, subtrees: list["GrammarTree"], text: str = "") -> None:
        self.root = {"label": label, "text": text}
        self.subtrees = subtrees

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.
        The indentation level is specified by the <depth> parameter.
        """
        if self.root == []:
            return ''
        else:
            if len(self.root["text"]) > 0:
                s = '  ' * depth + f'{self.root["label"]}: {self.root["text"]}\n'
            else:
                s = '  ' * depth + f'{self.root["label"]}\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def find_the_last(self) -> str:
        """Return the end punctuation of the sentence represented by the tree, if
        the sentence has an end punctuation. Otherwise, the returned string is
        the root['text'] value of the last subtree of this tree.
        Example usages see test_find_the_last() in tests_grammar_tree_methods.py.
        """
        s = self
        last = s.subtrees[-1]
        return last.root['text']

    def contain_type(self, kind: str) -> bool:
        """Return whether the entire tree contains the input type of constituent tag.
        Example usages see test_contain_type() in tests_grammar_tree_methods.py.
        """
        if self.root['label'] == kind:
            return True
        else:
            return any(i.contain_type(kind) for i in self.subtrees)

    def contain_content(self, word_or_punc: str) -> bool:
        """Return whether the entire tree contains the input word/punctuation mark.
        Example usages see test_contain_content() in tests_grammar_tree_methods.py.
        """
        if self.root['text'] == word_or_punc:
            return True
        else:
            return any(i.contain_content(word_or_punc) for i in self.subtrees)

    def get_sentence(self) -> str:
        """Returns the English sentence represented by the tree.
        Example usages see test_get_sentence() in tests_grammar_tree_methods.py.
        """
        if self.root["text"] != "":
            # self is a leaf
            return self.root["text"]
        else:
            sent_lst = []
            for subtree in self.subtrees:
                sent_lst.append(subtree.get_sentence())
            sent_lst = [v for v in sent_lst if v != ""]

            # remove the space between a word and a succeeding punctuation
            punc_index_lst = [i for i, x in enumerate(sent_lst) if x in {",", ".", "!", "?"}]
            sent_lst_partitioned = [sent_lst[i:j] for i, j in
                                    zip([0] + punc_index_lst, punc_index_lst + [None])]
            sent = ""
            for lst in sent_lst_partitioned:
                sent += " ".join(lst)
            return sent


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': [],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
