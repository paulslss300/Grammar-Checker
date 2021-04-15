"""
This file contains the GrammarTree class, which is a recursive tree data structure
that represents a constituent parse tree of an English sentence.

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""
from typing import Optional
import _grammar_checking_methods1 as gc1
import _grammar_checking_methods2 as gc2


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
    #       constituent parse tree this Grammar tree is representing. _subtrees is
    #       empty means this GrammarTree represents a constituent parse tree of a word.

    _root: dict[str: str]
    _subtrees: list["GrammarTree"]

    def __init__(self, label: str, subtrees: list, text: str = "") -> None:
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

    def plural_nouns_match_singular_verb_use(self) -> str:
        """
        Use the helper in _grammar_checking_methods1.py
        """
        return gc1.plural_nouns_match_singular_verb(self)

    def singular_noun_match_plural_verb_use(self) -> str:
        """
        Use the helper in _grammar_checking_methods1.py
        """
        return gc1.singular_noun_match_plural_verb(self)

    def check_noun_plural_and_singular_use(self) -> str:
        """
        Use the helper in _grammar_checking_methods1.py
        """
        return gc1.check_noun_plural_and_singular(self)

    def check_end_punctuations_use(self) -> str:
        """
        Use the helper in _grammar_checking_methods1.py
        """
        return gc1.check_end_punctuations(self)

    def existence_of_noun_use(self) -> str:
        """
        Use the helper in _grammar_checking_methods1.py
        """
        return gc1.existence_of_noun(self)

    def multiple_verbs_in_one_simple_sentence(self) -> str:
        """
        Use the helper in _grammar_checking_methods1.py
        """
        return gc1.multiple_verbs_in_one_simple_sentence(self)

    def a_complete_sentence_or_not(self) -> bool:
        """Use the helper in _grammar_checking_methods2.py"""
        return gc2.a_complete_sentence_or_not(self)

    def check_adj(self) -> Optional[str]:
        """Use the helper in _grammar_checking_methods2.py"""
        return gc2.check_adj(self)

    def check_vbg(self) -> Optional[str]:
        """Use the helper in _grammar_checking_methods2.py"""
        return gc2.check_vbg(self)

    def check_conjunction(self) -> Optional[str]:
        """Use the helper in _grammar_checking_methods2.py"""
        return gc2.check_conjunction(self)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['_grammar_checking_methods1', '_grammar_checking_methods2', 'typing'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })

# TODO: put into unit tests
# vbz2 = GrammarTree('VBZ', [], 'sings')
# vbz1 = GrammarTree('VBZ', [], 'runs')
# prp1 = GrammarTree('PRP', [], 'He')
# np1 = GrammarTree('NP', [prp1])
# vp1 = GrammarTree('VP', [vbz1, vbz2])10
# # USE THIS NOT THE ONE WITH ROOT
# mul_verb_ex1_1 = GrammarTree('S', [np1, vp1])
# # He runs sings
# mul_verb_and_punc_ex1 = GrammarTree('ROOT', [mul_verb_ex1_1])
#
#
# hate = GrammarTree('VBP', [], 'hate')
# it = GrammarTree('PRP', [], 'it')
# np2 = GrammarTree('NP', [it])
# vp2 = GrammarTree('VP', [hate, np2])
# period = GrammarTree('.', [], '.')
# # USE THIS NOT THE ONE WITH ROOT
# s1 = GrammarTree('S', [np1, vp2, period])
# # Contains pronoun. He hate it.
# s_noun_p_verb1 = GrammarTree('ROOT', [s1])
#
# dogs = GrammarTree('NNS', [], 'dogs')
# dogs_np = GrammarTree('NP', [dogs])
# # USE THIS NOT THE ONE WITH ROOT
# s2 = GrammarTree('S', [dogs_np, vp2, period])
# # Hard to determine. Dogs hate it.
# p_noun_s_verb2 = GrammarTree('ROOT', [s2])
#
# dog = GrammarTree('NN', [], 'dog')
# aaa = GrammarTree('DT', [], 'A')
# np3 = GrammarTree('NP', [dog, aaa])
# # USE THIS NOT THE ONE WITH ROOT
# s3 = GrammarTree('S', [np3, vp2, period])
# # Report it. A dog hate it.
# s_noun_p_verb3 = GrammarTree('ROOT', [s3])
#
# likes = GrammarTree('VBZ', [], 'likes')
# doing = GrammarTree('VBG', [], 'doing')
# that1 = GrammarTree('DT', [], 'that')
# np4 = GrammarTree('NP', [that1])
# vp3 = GrammarTree('VP', [doing, np4])
# s_small1 = GrammarTree('S', [vp3])
# vp4 = GrammarTree('VP', [likes, s_small1])
# # USE THIS NOT THE ONE WITH ROOT
# s4 = GrammarTree('S', [vp4])
# # Report it. likes doing that
# no_subject1 = GrammarTree('ROOT', [s4])
