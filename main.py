"""
This file contains comprehensive unit tests for the grammar checking methods.

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""

import pytest
from translator import translate


def test_nouns_single_verb1() -> None:
    """
    This test function test the method plural_noun_single_verb in file grammar_checking_tree.py
    """
    string1 = 'Many beautiful cars is in New York City.'
    test1 = translate(string1)[0]
    assert test1.plural_noun_singular_verb().message == \
           'A plural noun is mistakenly matched to a singular verb.'


def test_nouns_single_verb2() -> None:
    """
    This test function test the method plural_noun_single_verb in file grammar_checking_tree.py
    """
    string1 = 'Many beautiful cars is in New York City.'
    test1 = translate(string1)[0]
    assert test1.plural_noun_singular_verb().type_str == 'Possible Error'


def test_nouns_single_verb3() -> None:
    """
    This test function test the method plural_noun_single_verb in file grammar_checking_tree.py
    """
    string1 = 'Many beautiful cars is in New York City.'
    test1 = translate(string1)[0]
    assert test1.plural_noun_singular_verb().type == 2


def test_singular_noun_verbs1() -> None:
    """
    This test function test the method singular_noun_plural_verb in file grammar_checking_tree.py
    """
    string2 = 'This handsome professor have excellent reputation.'
    test2 = translate(string2)[0]
    assert test2.singular_noun_plural_verb().message == \
           'A singular noun is mistakenly matched to a plural verb.'


def test_singular_noun_verbs2() -> None:
    """
    This test function test the method singular_noun_plural_verb in file grammar_checking_tree.py
    """
    string2 = 'This handsome professor have excellent reputation.'
    test2 = translate(string2)[0]
    assert test2.singular_noun_plural_verb().type == 2


def test_singular_noun_verbs3() -> None:
    """
    This test function test the method singular_noun_plural_verb in file grammar_checking_tree.py
    """
    string2 = 'This handsome professor have excellent reputation.'
    test2 = translate(string2)[0]
    assert test2.singular_noun_plural_verb().type_str == 'Possible Error'


def test_check_noun_to_verb1() -> None:
    """
    This test function test the method check_noun_to_verb in file grammar_checking_tree.py
    """
    string3 = 'A girl are thinking and boys swims.'
    test3 = translate(string3)[0]
    assert test3.check_noun_to_verb().message == 'A singular noun is mistakenly matched to a ' \
                                                 'plural verb. A plural noun is mistakenly ' \
                                                 'matched to a singular verb.'


def test_check_noun_to_verb2() -> None:
    """
    This test function test the method check_noun_to_verb in file grammar_checking_tree.py
    """
    string3 = 'A girl are thinking and boys swims.'
    test3 = translate(string3)[0]
    assert test3.check_noun_to_verb().type == 2


def test_check_noun_to_verb() -> None:
    """
    This test function test the method check_noun_to_verb in file grammar_checking_tree.py
    """
    string3 = 'A girl are thinking and boys swims.'
    test3 = translate(string3)[0]
    assert test3.check_noun_to_verb().type_str == 'Possible Error'


def test_punctuation1() -> None:
    """
    This test function test the method check_end_punctuation in file grammar_checking_tree.py
    """
    string4 = 'Computer science is cool!'
    test4 = translate(string4)[0]
    assert (test4.check_end_punctuation().type == 1) and \
           (test4.check_end_punctuation().type_str == 'Error Undetected')


def test_punctuation2() -> None:
    """
    This test function test the method check_end_punctuation in file grammar_checking_tree.py
    """
    string4 = 'Computer science is cool'
    test4 = translate(string4)[0]
    assert (test4.check_end_punctuation().type == 2) and \
           (test4.check_end_punctuation().type_str == 'Possible Error') and \
           (test4.check_end_punctuation().message == "Sentence not ended with '.', '!' or '?'.")


def test_existence_of_subject() -> None:
    """
    This test function test the method existence_of_subject in file grammar_checking_tree.py
    """
    string5 = 'want to have a lunch.'
    test5 = translate(string5)[0]
    assert (test5.existence_of_subject().message == 'There is no subject in the sentence.') and \
           (test5.existence_of_subject().type == 2) and \
           (test5.existence_of_subject().type_str == 'Possible Error')


def test_complete_sentence() -> None:
    """This is the test function test the check_complete_sentence in file
    grammar_checking_tree.py"""
    string = 'She beautiful.'
    test = translate(string)[0]
    assert test.check_complete_sentence().type == 2


def test_check_adj1() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'He is cool.'
    test = translate(string)[0]
    assert test.check_adjective([]).type == 1


def test_check_adj2() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'She beautiful.'
    test = translate(string)[0]
    assert test.check_adjective([]).type == 2


def test_check_adj3() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man who is handsome has a cool car.'
    test = translate(string)[0]
    assert test.check_adjective([]).type == 1


def test_check_adj4() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man who happy play.'
    test = translate(string)[0]
    assert test.check_adjective([]).message == 'adj can not be adverb'


def test_check_adj5() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man who happy is Tom.'
    test = translate(string)[0]
    assert test.check_adjective([]).message == 'adj in wrong position, maybe lack linking-verb'


def test_check_adj6() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man happy is cool.'
    test = translate(string)[0]
    assert test.check_adjective([]).message == 'There may no linking verb before adj'


def test_check_adj7() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man has a dog.'
    test = translate(string)[0]
    assert test.check_adjective([]).message == 'no adj inside or use adj wrongly'


def test_check_adj8() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'Is he cool?'
    test = translate(string)[0]
    assert test.check_adjective([]).type == 1


def test_check_adj9() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'He is cool and has a cool'
    test = translate(string)[0]
    assert test.check_adjective([]).message == 'Noun may not follow the adj.'


def test_check_adj10() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'Is the man who is cool and has a nice car is crazy?'
    test = translate(string)[0]
    assert test.check_adjective([]).message == 'it is a question sentence and difficult to ' \
                                               'determinate'


def test_check_adj11() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man who is cool crazy.'
    test = translate(string)[0]
    assert test.check_adjective([]).message == 'can not easily judge: no error so far'


def test_check_verb1() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'He is swimming.'
    test = translate(string)[0]
    assert test.check_verb([]).type == 1


def test_check_verb2() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'He is cool.'
    test = translate(string)[0]
    assert test.check_verb([]).message == 'no verb_ing inside or use verb_ing incorrectly'


def test_check_verb3() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'He eats eating'
    test = translate(string)[0]
    assert test.check_verb([]).message == 'it may lack be-verb/like befor verb_ing'


def test_check_verb4() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'The man who likes eating and drinking.'
    test = translate(string)[0]
    assert test.check_verb([]).type == 1


def test_check_verb5() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'The man who likes eating drinking.'
    test = translate(string)[0]
    assert test.check_verb([]).message == 'can not easily judge'


def test_check_parallelism() -> None:
    """This is the test function test the check_parallelism in file grammar_checking_tree.py"""
    string = 'A cool and clever Canadian man.'
    test = translate(string)[0]
    assert test.check_parallelism().type == 1


def test_check_parallelism2() -> None:
    """This is the test function test the check_parallelism in file grammar_checking_tree.py"""
    string = 'A boy who is cool and likes drinking'
    test = translate(string)[0]
    assert test.check_parallelism().message == 'no detected error so far.'


if __name__ == '__main__':
    pytest.main(['main.py', '-v'])

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': [],
        'extra-imports': ['translator'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
