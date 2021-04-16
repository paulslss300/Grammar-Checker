"""
This file contains the GrammarCheckingTree class, which is a recursive tree data structure
that represents a constituent parse tree of an English sentence. This class has methods
for checking grammar rules.

This file is Copyright (c) 2021 Yuzhi Tang, Hongshou Ge, Zheng Luan.
"""
from grammar_tree import GrammarTree
from typing import Optional


class GrammarCheckingTree(GrammarTree):
    """Extends the GrammarTree class by adding grammar checking methods.
    """
    # Private Instance Attributes:
    #   - _subtrees:
    #       Stores a list of GrammarCheckingTree objects that represent children of the
    #       constituent parse tree this GrammarCheckingTree is representing. _subtrees is
    #       empty means this GrammarCheckingTree represents a constituent parse tree of a word.
    _subtrees: list["GrammarCheckingTree"]

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
                           'r6': self.multiverbs_match_mistake,
                           'r7': self.check_complete_sentence,
                           'r8': self.check_adjective,
                           'r9': self.check_verb,
                           'r10': self.check_parallelism}
        assert rules_lst == ["*"] or all(r in methods_mapping for r in rules_lst)

        feedback = []

        if rules_lst == ["*"]:
            checks_lst = list(methods_mapping.keys())
        else:
            checks_lst = rules_lst
        for rule in checks_lst:
            feedback.append(methods_mapping[rule]())
        return feedback

    # ----------------------------------------------------------------
    # ------------- Below are Joseph's methods ------------------------
    # ----------------------------------------------------------------

    def plural_noun_singular_verb(self) -> str:
        """As part of the subject-verb agreement rule, this method checks whether a
        plural noun is mistakenly matched to a singular verb and then return feedback.

        For some hard-to-determine situations, the feedback would not give a definite
        answer regarding the correctness of the sentence by this rule.

        Precondition:
            - The sentence does not start with a pronoun.
        """
        first = self
        while first._subtrees != []:
            first = first._subtrees[0]
        if first._root['label'] == 'PRP':
            return 'The subject is pronoun. This method can not determine.'
        result_mistake = 'This sentence may mistakenly match singular verb to plural nouns.'
        # Exist plural nouns. No and. No singular nouns. Exist third singular verb.
        if self.contain_type('NNS') and not self.contain_type('CC') \
                and not self.contain_type('NN') and self.contain_type('VBZ'):
            return result_mistake
        #  Only check sentences and sub-sentence.
        # for subtree in self.get_subtrees():
        for subtree in self._subtrees:
            if subtree._root['label'] == 'S':
                if subtree.plural_noun_singular_verb() == result_mistake:
                    return result_mistake
        return 'Maybe it is correct or it is hard to determine.'

    def singular_noun_plural_verb(self) -> str:
        """As part of the subject-verb agreement rule, this method checks whether a
        singular noun is mistakenly matched to a plural verb and then return feedback.

        For some hard-to-determine situations, the feedback would not give a definite
        answer regarding the correctness of the sentence by this rule.

        Precondition:
            - The sentence does not start with a pronoun.
        """
        first = self
        while first._subtrees != []:
            first = first._subtrees[0]
        if first._root['label'] == 'PRP':
            return 'The subject is pronoun. This method can not determine.'
        result_mistake = 'This sentence may mistakenly match plural verb to singular nouns.'
        # Exist singular Noun. No and. No plural nouns.
        # Exist verb phrase. Exist third singular verb.
        #
        if self.contain_type('NN') and not self.contain_type('NNS') and not \
                self.contain_type('CC') and self.contain_type('VP'):
            if not self.contain_type('VBD') and not self.contain_type('VBZ'):
                return result_mistake
        # Only check sentence and sub-sentence.
        for s in self._subtrees:
            if s._root['label'] == 'S':
                if s.singular_noun_plural_verb() == result_mistake:
                    return result_mistake
        return 'Maybe it is correct or it is hard to determine.'

    def check_noun_to_verb(self) -> str:
        """As part of the subject-verb agreement rule, this method uses 2 helpers to check
        whether a singular noun is mistakenly matched to a plural verb or whether a plural
        noun is mistakenly matched to a singular verb and then return feedback.

        For some hard-to-determine situations, the feedback would not give a definite
        answer regarding the correctness of the sentence by these 2 rules.

        Precondition:
            - The sentence does not start with a pronoun.
        """
        result_so_far = set()
        result_so_far.add(self.singular_noun_plural_verb())
        result_so_far.add(self.plural_noun_singular_verb())
        result_mistake1 = 'This sentence may mistakenly match singular verb to plural nouns.'
        result_mistake2 = 'This sentence may mistakenly match plural verb to singular nouns.'
        if result_mistake1 in result_so_far and result_mistake2 not in result_so_far:
            return result_mistake1
        elif result_mistake2 in result_so_far and result_mistake1 not in result_so_far:
            return result_mistake2
        elif result_mistake2 in result_so_far and result_mistake1 in result_so_far:
            return result_mistake2 + ' ' + result_mistake1
        else:
            return 'Maybe it is correct or it is hard to determine.'

    def check_end_punctuation(self) -> str:
        """Check whether the end punctuation of the sentence represented by the tree
        is correct and return feedback.
        """
        if not self.contain_content('!') and not self.contain_content('?') \
                and not self.contain_content('.'):
            return 'This sentence is not ended with exclamation mark, period mark or question mark.'
        if self.contain_type('SBARQ') or self.contain_type('SQ'):
            if self.find_the_last() == '?':
                return 'The question sentence ended correctly.'
        else:
            if self.find_the_last() == '.' or self.find_the_last() == '!':
                return 'This sentence has a good end punctuation.'
            else:
                return 'The end of this sentence is very likely to have a wrong punctuation.'
        return 'Something special happens. Can not detect this sentence.'

    def existence_of_subject(self) -> str:
        """Check whether this sentence has a subject.
        """
        if (self._root['label'] == 'ROOT' or self._root['label'] == 'S') \
                and not self.contain_type('NP'):
            return 'There is no subject in the sentence.'
        l_copy = self._subtrees.copy()
        l2 = l_copy.copy()
        for ss in l2:
            if ss._root['label'] == 'VP':
                l_copy.remove(ss)
        if any(i.contain_type('NP') for i in l_copy) is False:
            return 'There is likely being no subject in the sentence.'
        else:
            return 'Maybe it is correct or it is hard to determine.'

    def multiverbs_match_mistake(self) -> str:
        """Check whether a simple (combining) sentence contains more than one verb.
        TODO: edit docstring
        TODO: edit method name
        """
        result_a = 'There may be multiple verbs match to one noun in a simple sentence.'
        if not self.contain_type('VP'):
            return 'There is no verb phrase in this sentence.'
        the_sentence = self
        vp_lst = [tree for tree in the_sentence._subtrees if tree._root['label'] == 'VP']
        vb_set = {'VBZ', 'VBP', 'VBD', 'VBN', 'VP'}
        vb_use_set = {'VBZ', 'VBP', 'VBD'}
        for vp in vp_lst:
            l_copy = vp._subtrees.copy()
            for vbx in vp._subtrees:
                if vbx._root['label'] in vb_set:
                    l_copy.remove(vbx)
                    neo_l_copy = [i for i in l_copy if i._root['label'] in vb_use_set]
                    if neo_l_copy != []:
                        return result_a

        return 'No such kind of mistakes have been detected, yet.'

    # ----------------------------------------------------------------
    # ------------- Below are Caules' methods ------------------------
    # ----------------------------------------------------------------

    def check_complete_sentence(self) -> bool:
        """Check whether the sentence has noun and verb

        Precondition:
            - self.root['label'] == 'ROOT'

        """
        sentence = self._subtrees[0]
        if not (sentence.contain_type('NP') and sentence.contain_type('VP')):
            print('This is not a sentence because it lacks noun or verb')
            return False
        else:
            return True

    def check_adjective(self, whether_question: bool = False) -> Optional[str]:
        """According to the grammar book, the position of adj has 3 cases:
                    1. adj is before a noun
                    2. adj is after a linking verb
                """
        if self.contain_type('JJ') or self.contain_type('ADJP'):
            # check the type of self first
            if self._root['label'] == 'SQ':
                whether_question = True

            if self._root['label'] == 'JJ':
                if whether_question:
                    return 'This is a question sentence and hard to judge'
                else:
                    return 'hard to determinate: it may lack linking-verb or use adj incorrectly'

            if self._root['label'] == 'ADVP':
                return 'adj can not be adverb'

            if self._root['label'] == 'FRAG':
                return 'you may lacks some linking verb or noun around adj'

            if self._root['label'] == 'NP':
                # usually, adj before a noun

                for i in range(0, len(self._subtrees)):
                    # eg. He is a cool Canadian boy
                    if i != len(self._subtrees) - 1 and \
                            (self._subtrees[i]._root['label'] == 'JJ' or
                             self._subtrees[i]._root['label'] == 'ADJP') \
                            and (self._subtrees[i + 1]._root['label'] == 'NN' or
                                 self._subtrees[i + 1]._root['label'] == 'NNS'):
                        if not whether_question:
                            return ''
                        else:
                            return 'it is a question sentence and difficult to determinate'

                    # adj may after noun in question sentence: eg. is he cool?
                    elif i != len(self._subtrees) - 1 and \
                            (self._subtrees[i]._root['label'] == 'NN' or self._subtrees[i]._root[
                                'label'] == 'NNP' or self._subtrees[i]._root['label'] == 'NNS' or
                             self._subtrees[i]._root['label'] == 'NP') and \
                            (self._subtrees[i + 1]._root['label'] == 'JJ' or
                             self._subtrees[i + 1]._root[
                                 'label'] == 'ADJP'):
                        if whether_question:
                            return 'This is a question sentence and may no mistake'
                        else:
                            return 'There may no linking verb before adj'
                # adj not in self.subtree
                for x in self._subtrees:
                    result = x.check_adjective(whether_question)
                    if result != '':
                        return result

                return 'can not easily judge'

            elif self._root['label'] == 'VP':
                # adj must follow the verb
                if self._subtrees[0]._root['label'] == 'JJ':
                    # This must be wrong because the VP starts with a adj
                    return "adj in wrong position"

                # usually, it should be linking-verb + adj
                if self._subtrees[1]._root['label'] == 'JJ' or \
                        self._subtrees[1]._root['label'] == 'ADJP' and \
                        self._subtrees[0]._root['text'] == 'am' or self._subtrees[0]._root[
                    'text'] == 'is' or self._subtrees[0]._root['text'] == 'are' or \
                        self._subtrees[0]._root['text'] == 'was' or \
                        self._subtrees[0]._root['text'] == 'were':
                    # eg. The man is cool.
                    if not whether_question:
                        return ''
                    # is the man cool?
                    else:
                        return 'this is a question sentence and difficult to judge'
                else:
                    # NP may in the subtree of VP. eg. He is a cool Canadian boy.
                    for x in self._subtrees:
                        result = x.check_adjective(whether_question)
                        if result != '':
                            return result

                    return 'can not easily judge'
            else:
                # adj not in self.subtree.
                for x in self._subtrees:
                    result = x.check_adjective(whether_question)
                    if result != '':
                        return result

        else:
            return ''

    def check_verb(self) -> Optional[str]:
        """check the verb_ing form
        case1: be-verb/like + verbing
        """

        if self.contain_type('VBG'):
            # check the type of self
            if self._root['label'] == 'VBG':
                return 'it is hard to determinate'

            if self._root['label'] == 'SQ':
                # question sentence eg. is he swimming?
                return 'This is a question sentence and hard to judge'

            if self._root['label'] == 'SBAR':
                for x in self._subtrees:
                    result = x.check_verb()
                    if result != '':
                        return result

            if self._root['label'] == 'VP' and any(
                    x._root['label'] == 'VBG' for x in self._subtrees):
                # if VBG is in the subtree of self(a VP)

                if self._subtrees[0]._root['label'] == 'VBG':
                    # if VP starts with a vbg
                    return 'This may be true or lacks be/like or use verbing incorrectly'

            # If VP contains VBG
            elif self._root['label'] == 'VP' or self._root['label'] == 'S':
                if self._subtrees[0]._root['text'] == 'am' or \
                        self._subtrees[0]._root[
                            'text'] == 'is' or self._subtrees[0]._root['text'] == 'are' or \
                        self._subtrees[0]._root['text'] == 'was' or self._subtrees[0]._root[
                    'text'] == 'were' or self._subtrees[0]._root['text'] == 'like' or \
                        self._subtrees[0]._root['text'] == 'likes' and \
                        self._subtrees[1]._subtrees[0]._root['label'] == 'VBG':
                    # be/like + verbing
                    return ''
                for x in self._subtrees:
                    result = x.check_verb()
                    if result != '':
                        return result

            # vbg not in self.subtree
            for x in self._subtrees:
                result = x.check_verb()
                if result != '':
                    return result

        else:
            return ''

    def check_parallelism(self) -> Optional[str]:
        """Check whether both sides of the conjunction are parallel """
        if self.contain_type('CC'):
            for i in range(0, len(self._subtrees)):
                if self._subtrees[i]._root['label'] == 'CC' and \
                        self._subtrees[i - 1]._subtrees != self._subtrees[i + 1]._subtrees:
                    # if they are parallel, the elements in there subtrees are the same.
                    return 'hard to determinate: the left side of ' \
                           'the conjunction is not parallel to the right side.'

            for x in self._subtrees:
                return x.check_parallelism()

        else:
            return


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['grammar_tree', 'typing'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
