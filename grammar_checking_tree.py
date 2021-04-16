"""
This file contains the GrammarCheckingTree class, which is a recursive tree data structure
that represents a constituent parse tree of an English sentence. This class has methods
for checking grammar rules.

This file also contains the Feedback class, which represents a grammar-checking
feedback returned by the grammar-checking methods in GrammarCheckingTree.

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""
from typing import Optional
from grammar_tree import GrammarTree


class Feedback:
    """
    This class represents a grammar-checking feedback returned by the grammar-
    checking methods in GrammarCheckingTree.

    Instance Attributes:
        - type: integer representing the type of feedback.
        - type: string description of the type of feedback.
        - message: message accompanied with the feedback.

    Representation Invariants:
        - self.type in {"Possible Error", "Test Ineffective", "Error Undetected"}
    """
    type: int
    type_str: str
    message: str

    def __init__(self, type: int, msg: str = "") -> None:
        """
        Precondition:
            - type in [1, 2, 3]
        """
        assert type in [1, 2, 3]
        type_map = {1: "Error Undetected", 2: "Possible Error", 3: "Test Ineffective"}
        self.type = type
        self.type_str = type_map[type]
        self.message = msg


class GrammarCheckingTree(GrammarTree):
    """Extends the GrammarTree class by adding grammar checking methods.

    Instance Attributes:
        - subtrees:
            Stores a list of GrammarCheckingTree objects that represent children of the
            constituent parse tree this GrammarCheckingTree is representing. _subtrees is
            empty means this GrammarCheckingTree represents a constituent parse tree of a word.
    """
    subtrees: list["GrammarCheckingTree"]

    def __init__(self, label: str, subtrees: list["GrammarCheckingTree"], text: str = "") -> None:
        super().__init__(label, subtrees, text)

    def check_selected_rules(self, rules_lst: list[str]) -> [str]:
        """Checks the selected grammar rules on the tree and return feedback.
        Note that if the input list contains only "*", the function checks all
        implemented grammar rules on the tree and return feedback.

        Preconditions:
            - every element in rules_lst are keys in methods_mapping or
            rules_lst == ["*"].
        """
        methods_mapping = {'r1': self.plural_noun_singular_verb,
                           'r2': self.singular_noun_plural_verb,
                           'r3': self.check_noun_to_verb,
                           'r4': self.check_end_punctuation,
                           'r5': self.existence_of_subject,
                           # 'r6': self.check_complete_sentence,
                           # 'r7': self.check_adjective,
                           # 'r8': self.check_verb,
                           # 'r9': self.check_parallelism
                           }
        assert rules_lst == ["*"] or all(r in methods_mapping for r in rules_lst)

        feedback = []

        if rules_lst == ["*"]:
            checks_lst = list(methods_mapping.keys())
        else:
            checks_lst = rules_lst
        for rule in checks_lst:
            fb = methods_mapping[rule]()
            if fb.message == "":
                feedback.append(f'{rule}: {fb.type_str}.')
            else:
                feedback.append(f'{rule}: {fb.type_str}. {fb.message}')
        return feedback

    # ----------------------------------------------------------------
    # ------------- Below are Joseph's methods ------------------------
    # ----------------------------------------------------------------

    def plural_noun_singular_verb(self) -> Feedback:
        """As part of the subject-verb agreement rule, this method checks whether a
        plural noun is mistakenly matched to a singular verb and then return feedback.

        E.g. "The ships sail away." is wrong while "The ships sails away." is correct.

        IMPORTANT: This method may be ineffective for certain sentence types (see
        Discussion in project report).

        Example usages see TODO in main.py.

        Precondition:
            - The sentence does not start with a pronoun as the subject.
        """
        first = self
        while first.subtrees != []:
            first = first.subtrees[0]
        if first.root['label'] == 'PRP':
            return Feedback(3, 'The sentence starts with a pronoun as the subject.')
        err_feedback = Feedback(2, 'A plural noun is mistakenly matched to a singular verb.')
        # Exist plural nouns. No and. No singular nouns. Exist third singular verb.
        if self.contain_type('NNS') and not self.contain_type('CC') \
                and not self.contain_type('NN') and self.contain_type('VBZ'):
            return err_feedback
        #  Only check sentences and sub-sentence.
        # for subtree in self.get_subtrees():
        for subtree in self.subtrees:
            if subtree.root['label'] == 'S':
                if subtree.plural_noun_singular_verb().type == 2:
                    return err_feedback
        return Feedback(1)

    def singular_noun_plural_verb(self) -> Feedback:
        """As part of the subject-verb agreement rule, this method checks whether a
        singular noun is mistakenly matched to a plural verb and then return feedback.

        E.g. "The ship sail away." is wrong while "The ship sails away." is correct.

        IMPORTANT: This method may be ineffective for certain sentence types (see
        Discussion in project report).

        Example usages see TODO in main.py.

        Precondition:
            - The sentence does not start with a pronoun.
        """
        first = self
        while first.subtrees != []:
            first = first.subtrees[0]
        if first.root['label'] == 'PRP':
            return Feedback(3, 'The sentence starts with a pronoun as the subject.')
        err_feedback = Feedback(2, 'A singular noun is mistakenly matched to a plural verb.')
        # Exist singular Noun. No and. No plural nouns.
        # Exist verb phrase. Exist third singular verb.
        if self.contain_type('NN') and not self.contain_type('NNS') and not \
                self.contain_type('CC') and self.contain_type('VP'):
            if not self.contain_type('VBD') and not self.contain_type('VBZ'):
                return err_feedback
        # Only check sentence and sub-sentence.
        for s in self.subtrees:
            if s.root['label'] == 'S':
                if s.singular_noun_plural_verb() == 2:
                    return err_feedback
        return Feedback(1)

    def check_noun_to_verb(self) -> Feedback:
        """As part of the subject-verb agreement rule, this method uses 2 helpers to check
        whether a singular noun is mistakenly matched to a plural verb or whether a plural
        noun is mistakenly matched to a singular verb and then return feedback.

        IMPORTANT: This method may be ineffective for certain sentence types (see
        Discussion in project report).

        Example usages see TODO in main.py.

        Precondition:
            - The sentence does not start with a pronoun.
        """
        feedback1 = self.singular_noun_plural_verb()
        feedback2 = self.plural_noun_singular_verb()
        feedback_type = max(feedback1.type, feedback2.type)
        if feedback1.message == feedback2.message:
            msg = feedback1.message
        elif feedback1.message == "":
            msg = feedback2.message
        elif feedback2.message == "":
            msg = feedback1.message
        else:
            msg = feedback1.message + ", and " + feedback2.message
        return Feedback(feedback_type, msg)

    def check_end_punctuation(self) -> Feedback:
        """Check whether the end punctuation of the sentence represented by the tree
        is correct and return feedback. End punctuation in this case refers to only
        ".", "!", and "?".

        E.g. "What is he doing." does not have correct end punctuation as it should
        have been ended with "?". "He is good" also does not have correct end punctuation
        as it lacks an end punctuation. "He is good." does have correct end punctuation.

        IMPORTANT: This method may be ineffective for certain sentence types (see
        Discussion in project report).

        Example usages see TODO in main.py.
        """
        if not self.contain_content('!') and not self.contain_content('?') \
                and not self.contain_content('.'):
            return Feedback(2, "Sentence not ended with '.', '!' or '?'.")
        if self.contain_type('SBARQ') or self.contain_type('SQ'):
            if self.find_the_last() == '?':
                return Feedback(1, "Sentence has a good end punctuation.")
        else:
            if self.find_the_last() == '.' or self.find_the_last() == '!':
                return Feedback(1, "Sentence has a good end punctuation.")
            else:
                return Feedback(2, "Sentence has a wrong punctuation.")
        return Feedback(3, 'Something special happens. Can not detect this sentence.')

    def existence_of_subject(self) -> Feedback:
        """Check whether this sentence has a subject.

        IMPORTANT: This method may be ineffective for certain sentence types (see
        Discussion in project report).

        Example usages see TODO in main.py.
        """
        if self.root['label'] == 'S' and not self.contain_type('NP'):
            return Feedback(2, 'There is no subject in the sentence.')
        l_copy = self.subtrees.copy()
        l2 = l_copy.copy()
        for ss in l2:
            if ss.root['label'] == 'VP':
                l_copy.remove(ss)
        if any(i.contain_type('NP') for i in l_copy) is False:
            return Feedback(2, 'There is no subject in the sentence.')
        else:
            return Feedback(1, "There is likely a subject in the sentence.")

    # ----------------------------------------------------------------
    # ------------- Below are Caules' methods ------------------------
    # ----------------------------------------------------------------
# Check whether the sentence represented by the tree has a noun phrase
#             and a verb phrase (i.e. minimum requirement for the sentence to be
#             complete).

    def check_complete_sentence(self) -> Feedback:
        """Check whether the sentence represented by the tree has a noun phrase
        and a verb phrase (i.e. minimum requirement for the sentence to be
        complete).
        """
        if not (self.contain_type('NP') and self.contain_type('VP')):
            return Feedback(2, "Sentence is incomplete.")
        else:
            return Feedback(1, "Sentence is complete.")

    def check_adjective(self, whether_question: Optional[bool] = False) -> Optional[str]:
        """According to the grammar book, the position of adj has 2 cases:
                    1. adj is before a noun
                    2. adj is after a linking verb
                """
        if self.contain_type('JJ') or self.contain_type('ADJP'):
            # check the type of self first
            if self.root['label'] == 'SQ':
                whether_question = True

            if self.root['label'] == 'JJ':
                if whether_question:
                    return 'This is a question sentence and hard to judge'
                else:
                    return 'hard to determinate: it may lack linking-verb or use adj incorrectly'

            if self.root['label'] == 'ADVP':
                return 'adj can not be adverb'

            if self.root['label'] == 'FRAG':
                return 'you may lacks some linking verb or noun around adj'

            if self.root['label'] == 'NP':
                # usually, adj before a noun

                for i in range(0, len(self.subtrees) - 1):
                    # eg. He is a cool Canadian boy
                    # noun is not followed the adj or adjp(cool and young).
                    # eg. A [cool and young](adjp) boy/ a cool boy.

                    condition1 = self.subtrees[i].root['label'] == 'JJ' or self.subtrees[i] \
                        .root['label'] == 'ADJP'
                    condition2 = self.subtrees[i + 1].root['label'] == 'NN' or self. \
                        subtrees[i + 1].root['label'] == 'NNS'
                    if condition1 and condition2:
                        if whether_question:
                            return 'it is a question sentence and difficult to determinate'
                        else:
                            return None
                    # adj may after noun in question sentence: eg. is he cool?
                    condition3 = (self.subtrees[i].root['label'] == 'NN'
                                  or self.subtrees[i].root['label']
                                  == 'NNP' or self.subtrees[i].root['label'] == 'NNS' or self.
                                  subtrees[i].root['label'] == 'NP')
                    condition4 = (self.subtrees[i + 1].root['label'] == 'JJ'
                                  or self.subtrees[i + 1].
                                  root['label'] == 'ADJP')
                    if condition3 and condition4:
                        if whether_question:
                            return 'This is a question sentence and may no mistake'
                        else:
                            return 'There may no linking verb before adj'
                # if adj not in self._subtree
                for x in self.subtrees:
                    result = x.check_adjective(whether_question)
                    if result != 'no adj inside or use adj wrongly':
                        return result

                return 'can not easily judge: no error so far'

            elif self.root['label'] == 'VP' or self.root['label'] == 'S':
                # adj must follow the verb
                if self.subtrees[0].root['label'] == 'JJ':
                    # This must be wrong because the VP starts with a adj
                    return "adj in wrong position, maybe lack linking-verb"
                # usually, it should be linking-verb + adj
                condition5 = self.subtrees[0].root['text'] == 'am' or self.subtrees[0].root[
                    'text'] == 'is' or self.subtrees[0].root['text'] == 'are' or self.subtrees[0] \
                                 .root['text'] == 'was' or self.subtrees[0].root['text'] == 'were'
                if self.subtrees[1].root['label'] == 'JJ' \
                        or self.subtrees[1].root['label'] == 'ADJP' \
                        and condition5:
                    # eg. The man is cool.
                    if whether_question:
                        return 'this is a question sentence and difficult to judge'
                    else:
                        return None
                else:
                    # if adj not in self._subtree
                    for x in self.subtrees:
                        result = x.check_adjective(whether_question)
                        if result != 'no adj inside or use adj wrongly':
                            return result
                    return 'can not easily judge: no error so far'
            else:
                # not types listed above
                for x in self.subtrees:
                    result = x.check_adjective(whether_question)
                    if result != 'no adj inside or use adj wrongly':
                        return result
            return 'can not easily judge: no error so far'

        else:
            return 'no adj inside or use adj wrongly'

    def check_verb(self) -> Optional[str]:
        """check the verb_ing form
        case1: be-verb/like + verbing
        """

        if self.contain_type('VBG'):
            # check the type of self
            if self.root['label'] == 'VBG':
                return 'it is hard to determinate'

            if self.root['label'] == 'SQ':
                # question sentence eg. is he swimming?
                return 'This is a question sentence and hard to judge'

            if self.root['label'] == 'SBAR':
                for x in self.subtrees:
                    result = x.check_verb()
                    if result != 'no verb_ing inside':
                        return result

            # if VBG is in the subtree of VP
            if self.root['label'] == 'VP' and any([sub.root['label'] == 'VBG' for sub
                                                   in self.subtrees]):
                if self.subtrees[0].root['label'] == 'VBG':
                    # if VP starts with a vbg
                    return 'This may lack be/like or use verbing incorrectly'

            # If VP contains VBG
            elif self.root['label'] == 'VP' or self.root['label'] == 'S':
                condition1 = self.subtrees[0].root['text'] == 'am' or self. \
                    subtrees[0].root['text'] == 'is' or self.subtrees[0].root['text'] == 'are' \
                             or self.subtrees[0].root['text'] == 'was'
                # be/like + verbing
                if condition1 and self.subtrees[1].subtrees[0].root['label'] == 'VBG':
                    return None
                if self.subtrees[0].root[
                    'text'] == 'were' or self.subtrees[0].root['text'] == 'like' \
                        or self.subtrees[0].root['text'] == 'likes' \
                        and self.subtrees[1].subtrees[0].subtrees[0].root['label'] == 'VBG':
                    return None
                # vbg not in self.subtree
                for x in self.subtrees:
                    result = x.check_verb()
                    if result != 'no verb_ing inside':
                        return result

            # not types listed above
            for x in self.subtrees:
                result = x.check_verb()
                if result != 'no verb_ing inside':
                    return result

            return 'can not easily judge: no error so far'

        else:
            return 'no verb_ing inside'

    def check_parallelism(self) -> Optional[str]:
        """Check whether both sides of the conjunction are parallel """
        if self.contain_type('CC'):
            for i in range(0, len(self.subtrees)):
                if self.subtrees[i].root['label'] == 'CC' and \
                        self.subtrees[i - 1].subtrees != self.subtrees[i + 1].subtrees:
                    # if they are parallel, the number of elements in their subtrees are the same.
                    return 'hard to determinate: the left side of ' \
                           'the conjunction is not parallel to the right side.'

            for x in self.subtrees:
                x.check_parallelism()

            return None

        else:
            return None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['grammar_tree', 'typing'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
