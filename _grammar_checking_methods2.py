"""
This file only contains four grammar checking methods.
The classes we need will be stored in GrammarTree.py. I will import that file first.
"""
from __future__ import annotations

from typing import Optional


def a_complete_sentence_or_not(self) -> bool:
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


def check_adj(self, whether_question=False) -> Optional[str]:
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
                result = x.check_adj(whether_question)
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
                    result = x.check_adj(whether_question)
                    if result != '':
                        return result

                return 'can not easily judge'
        else:
            # adj not in self.subtree.
            for x in self._subtrees:
                result = x.check_adj(whether_question)
                if result != '':
                    return result

    else:
        return ''


def check_vbg(self) -> Optional[str]:
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
                result = x.check_vbg()
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
                result = x.check_vbg()
                if result != '':
                    return result

        # vbg not in self.subtree
        for x in self._subtrees:
            result = x.check_vbg()
            if result != '':
                return result

    else:
        return ''


def check_conjunction(self) -> Optional[str]:
    """Check whether both sides of the conjunction are parallel """
    if self.contain_type('CC'):
        for i in range(0, len(self._subtrees)):
            if self._subtrees[i]._root['label'] == 'CC' and \
                    self._subtrees[i - 1]._subtrees != self._subtrees[i + 1]._subtrees:
                # if they are parallel, the elements in there subtrees are the same.
                return 'hard to determinate: the left side of ' \
                       'the conjunction is not parallel to the right side.'

        for x in self._subtrees:
            return x.check_conjunction()

    else:
        return

