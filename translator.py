"""
This file contains the translate() function that converts a passage of English text into
GrammarTree object(s).

Note that I have accessed protected members of a class in _create_grammar_tree() and
_debugger(). This is unfortunately THE way to do it (at least for now), as outlined
in the documentation of benepar (https://pypi.org/project/benepar/):

"Since spaCy does not provide an official constituency parsing API, all methods are
accessible through the extension namespaces Span._ and Token._"

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""
from typing import Any, Dict
import benepar
import spacy
from grammar_tree import GrammarTree

# download and load parsing model
spacy.cli.download("en_core_web_md")
benepar.download('benepar_en3')
nlp = spacy.load("en_core_web_md")
nlp.add_pipe("benepar", config={"model": "benepar_en3"})


def translate(text: str) -> [GrammarTree]:
    """Return a list of GrammarTree object (each GrammarTree object represents a sentence)
    based on the input text using the benepar library.

    Precondition:
        - text can only contain letters in the English alphabet and basic
        punctuation marks (e.g. ",", ".", "?", "!").
    """
    grammar_trees = []

    doc = nlp(text)
    sentence_trees = list(doc.sents)
    for sentence_tree in sentence_trees:
        grammar_trees.append(_create_grammar_tree(sentence_tree))

    return grammar_trees


def _create_grammar_tree(tree: Any) -> GrammarTree:
    """Return a GrammarTree object for the given constituent parse tree object
    outputted by the benepar library.

    From the documentation, spaCy does not provide an official constituency parsing API,
    so all methods are only accessible through the extension namespaces Span._ and Token._.

    Preconditions:
        - tree is a constituent parse tree object outputted by the benepar library.
    """
    # sums up the number of children of tree (tree._.children is an iterator)
    if sum(1 for _ in tree._.children) == 0:
        parse_string_lst = str(tree._.parse_string).replace("(", "").replace(")", "").split()
        assert 2 <= len(parse_string_lst)
        # if len(parse_string_lst) == 2, tree represents a word (i.e. tree is a leaf)
        # if len(parse_string_lst) > 2, tree represents a unary chain of length
        # len(parse_string_lst) - 1 (special case)
        if len(parse_string_lst) == 2:
            label, text = parse_string_lst[0], parse_string_lst[1]
        else:
            dict_lst = []
            for parse_str in parse_string_lst[:-2]:
                dict_lst.append({"label": parse_str, "text": ""})
            dict_lst.append({"label": parse_string_lst[-2], "text": parse_string_lst[-1]})
            return _create_grammar_tree_lst(dict_lst)
    else:
        # tree represents a clause or a phrase that is not a unary chain
        label, text = str(tree._.labels[0]), ""

    grammar_tree = GrammarTree(label,
                               [_create_grammar_tree(subtree) for subtree in tree._.children],
                               text)
    return grammar_tree


def _create_grammar_tree_lst(lst: [Dict]) -> GrammarTree:
    """Return a GrammarTree that is a chain (i.e. the root and every subtree in the
    GrammarTree has only 1 child) based on the input list of dictionaries. For each
    dictionary in the input list, the dictionary at index i + 1 is the _root value of
    a GrammarTree that is the child of the GrammarTree whose _root value is the dictionary
    at index i.

    Precondition:
        - len(lst) >= 1
        - the keys of every dictionary in lst are "label" and "text" and their
        values are strings.
    """
    if len(lst) == 1:
        return GrammarTree(lst[0]["label"], [], lst[0]["text"])
    else:
        return GrammarTree(lst[0]["label"], [_create_grammar_tree_lst(lst[1:])], lst[0]["text"])


def _debugger(sentence: str) -> None:
    """Used as debugger tool for the developers."""
    doc = nlp(sentence)
    tree = list(doc.sents)[0]

    for constituent in tree._.constituents:
        cons_type = str(type(constituent))
        parse_str = str(constituent._.parse_string)
        children = list(constituent._.children)
        labels = str(constituent._.labels)
        print(f"type: {cons_type},"
              f"parse_string: {parse_str}, "
              f"children: {children}, "
              f"labels: {labels}")
        print("=========")


def examples() -> None:
    """Print out (to the console) examples of translations of English text into
    GrammarTree objects using the translate() function.

    To see what the labels mean in the printed tree, check out:
    http://www.surdeanu.info/mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html
    """
    # example 1 taken from https://lingua.com/english/reading/wonderful-family/ and modified
    example1 = "I live in a house near the mountains. " \
               "I have two brothers and one sister, and I was born last. " \
               "My grandmother cooks the best food! " \
               "She is seventy-eight?"
    grammar_trees_1 = translate(example1)
    for grammar_tree in grammar_trees_1:
        print(grammar_tree)
    print("==========")

    example2 = "The quick brown fox jumped over the lazy dog."
    grammar_trees_2 = translate(example2)
    for grammar_tree in grammar_trees_2:
        print(grammar_tree)


if __name__ == '__main__':
    examples()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E9997'],
        'extra-imports': ['typing', 'benepar', 'spacy', 'grammar_tree'],
        'allowed-io': ['examples', '_debugger'],
        'max-nested-blocks': 4
    })
