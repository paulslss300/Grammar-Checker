"""
This file contains some test functions for the grammar checking methods.
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

    
def test_check_adj1() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'He is cool.'
    test = translate(string)[0]
    assert test.check_adj().type == 1


def test_check_adj2() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'She beautiful.'
    test = translate(string)[0]
    assert test.check_adj().type == 2


def test_check_adj3() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man who is handsome has a cool car.'
    test = translate(string)[0]
    assert test.check_adj().type == 1


def test_check_adj4() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man who happy play.'
    test = translate(string)[0]
    assert test.check_adj().message == 'adj can not be adverb'


def test_check_adj5() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man who happy is Tom.'
    test = translate(string)[0]
    assert test.check_adj().message == 'adj in wrong position, maybe lack linking-verb'


def test_check_adj6() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man happy is cool.'
    test = translate(string)[0]
    assert test.check_adj().message == 'There may no linking verb before adj'


def test_check_adj7() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'The man has a dog.'
    test = translate(string)[0]
    assert test.check_adj().message == 'no adj inside or use adj wrongly'


def test_check_adj8() -> None:
    """This is the test function test the check_adj in file grammar_checking_tree.py"""
    string = 'Is he cool?'
    test = translate(string)[0]
    assert test.check_adj().type == 1


def test_check_verb1() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'He is swimming.'
    test = translate(string)[0]
    assert test.check_adj().type == 1


def test_check_verb2() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'He is cool.'
    test = translate(string)[0]
    assert test.check_adj().message == 'no verb_ing inside or use verb_ing incorrectly'


def test_check_verb3() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'He eats eating'
    test = translate(string)[0]
    assert test.check_adj().type == 2


def test_check_verb4() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'The man who likes eating and drinking.'
    test = translate(string)[0]
    assert test.check_adj().type == 1


def test_check_verb5() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'The man who likes eating drinking.'
    test = translate(string)[0]
    assert test.check_adj().messate == 'it is hard to determinate'


def test_check_parallelism() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'A cool and clever Canadian man.'
    test = translate(string)[0]
    assert test.check_adj().type == 1


def test_check_parallelism2() -> None:
    """This is the test function test the check_verb in file grammar_checking_tree.py"""
    string = 'A cool and clever Canadian man.'
    test = translate(string)[0]
    assert test.check_adj().message == 'hard to determinate: the left side of the conjunction ' \
                                       'is not parallel to the right side.'


if __name__ == '__main__':
    pytest.main(['main.py', '-v'])

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': [],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
