"""
This file contains unit tests for some methods of the GrammarTree class.

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""
from translator import translate


def test_find_the_last() -> None:
    """Unit tests for GrammarTree.find_the_last()."""
    tree = translate("Are you mad?")[0]
    assert tree.find_the_last() == "?"

    tree = translate("He is mad")[0]
    assert tree.find_the_last() == tree.get_subtrees()[-1].get_root()["text"]


def test_contain_type() -> None:
    """Unit tests for GrammarTree.contain_type()."""
    tree = translate("He eats food.")[0]
    assert tree.contain_type("VP")  # "eats food" constitutes as a VP (verb phrase)
    assert tree.contain_type("NN")  # "food" constitutes as a NN (singular noun)
    assert not tree.contain_type("JJ")  # nothing constitutes as a JJ (adjective)


def test_contain_content() -> None:
    """Unit tests for GrammarTree.contain_content()."""
    tree = translate("The brown fox jumped over the lazy dog.")[0]
    assert tree.contain_content("lazy")
    assert tree.contain_content(".")
    assert not tree.contain_content("?")
    assert not tree.contain_content("dogs")


if __name__ == '__main__':
    import pytest
    pytest.main(['tests_grammar_tree_methods.py'])

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': [],
        'extra-imports': ['translator'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })