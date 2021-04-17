"""
This file contains the demo grammar checking python program.

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""
from translator import translate


def demo_check_grammar(text: str, rules: list[str]) -> None:
    """Checks the selected grammar rules on the input English text and print feedback.
    Note that if the input list contains only "*", the function checks all
    implemented grammar rules on the tree and return feedback.

    Note that this demo grammar checker program works better with simpler and
    shorter sentences. In the future, grammar checking methods will be
    enhanced to produce better results for more complicated and longer
    sentences as well.

    Preconditions:
        - every element in rules are keys in methods_mapping defined in
        check_selected_rules in grammar_checking_tree.py or rules_lst == ["*"].
        - text != ""
    """
    trees = translate(text)
    for tree in trees:
        print(f'Sentence: {tree.get_sentence()}')
        feedbacks = tree.check_selected_rules(rules)
        for feedback in feedbacks:
            print(feedback)
    print("=====")


def example() -> None:
    """Print out (to the console) an example of grammar checking using
    demo_check_grammar.
    """
    sentence = "The foxes jumps over"
    # 2 errors in sentence:
    # 1) foxes + jumps
    # 2) no end punctuation
    demo_check_grammar(sentence, ["*"])


if __name__ == '__main__':
    example()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': [],
        'extra-imports': ['translator'],
        'allowed-io': ['demo_check_grammar'],
        'max-nested-blocks': 4
    })
