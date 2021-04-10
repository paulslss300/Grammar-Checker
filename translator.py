"""
This file contains the translate() function that converts a passage of English text into
GrammarTree object(s). # TODO: add copyright info
"""
from typing import Any
import benepar
import spacy
from t1 import GrammarTree # TODO: link to GrammarTree.py


# download and load parsing model
spacy.cli.download("en_core_web_md")
benepar.download('benepar_en3')
nlp = spacy.load("en_core_web_md")
nlp.add_pipe("benepar", config={"model": "benepar_en3"})


def translate(text: str) -> [GrammarTree]:
    """Create a list of GrammarTree object (each GrammarTree object represents a sentence)
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
    """Create a GrammarTree object for the given constituent parse tree object
    outputted by the benepar library.

    From the documentation, spaCy does not provide an official constituency parsing API,
    so all methods are only accessible through the extension namespaces Span._ and Token._.

    Preconditions:
        - tree is a constituent parse tree object outputted by the benepar library.
    """
    # sums up the number of children of tree (tree._.children is an iterator)
    if sum(1 for _ in tree._.children) == 0:
        parse_string_lst = str(tree._.parse_string).replace("(", "").replace(")", "").split()
        assert 2 <= len(parse_string_lst) <= 3
        # if len(parse_string_lst) == 2, tree represents a word (i.e. tree is a leaf)
        # if len(parse_string_lst) == 3, tree represents a unary chain of length 2 (special case)
        if len(parse_string_lst) == 2:
            label, text = parse_string_lst[0], parse_string_lst[1]
        else:
            leaf = GrammarTree(parse_string_lst[1], [], parse_string_lst[2])
            return GrammarTree(parse_string_lst[0], [leaf], "")
    else:
        # tree represents a clause or a phrase that is not a unary chain
        label, text = str(tree._.labels[0]), ""

    grammar_tree = GrammarTree(label,
                               [_create_grammar_tree(subtree) for subtree in tree._.children],
                               text)
    return grammar_tree


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
