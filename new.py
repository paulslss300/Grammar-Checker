from __future__ import annotations
from typing import Optional


class GrammarTree:
    """
        A recursive tree data structure that represents a constituent parse tree of an
        English sentence.

        Representation Invariants:
            - (self._subtrees == []) == (self._root["text"] != "")
            - self._root["text"] == "" or self._root["text"] is an English word or valid punctuation.
            - This sentence will not contains single quote marks, double quote mark or any citation.
            - all checking grammar method should have a input with _root['label'] == 'ROOT'
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
    _subtrees: list['GrammarTree']

    def __init__(self, label: str, subtrees: list, text: str = '') -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """

        self._root = {'label': label, 'text': text}
        self._subtrees = subtrees

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
                # Note that the 'depth' argument to the recursive call is modified.
                s += subtree._str_indented(depth + 1)
            return s

    def contain_type(self, kind: str) -> bool:
        """
        Judge the existence of a kind of tree.
        """
        if self._root['label'] == kind:
            return True
        else:
            return any(i.contain_type(kind) for i in self._subtrees)

    def a_complete_sentence_or_not(self) -> bool:
        """Check whether the sentence has noun and verb

        Precondition:
            - self.root['label'] == 'ROOT'

        """
        sentence = self._subtrees[0]
        if not (sentence.contain_type('NP') and sentence.contain_type('VP')):

            return False
        else:
            return True

    def check_adj(self, whether_question: Optional[bool] = False) -> Optional[str]:
        """According to the grammar book, the position of adj has 3 cases:
                    1. adj is before a noun
                    2. adj is after a linking verb
                    3. adj is after a noun or an indefinite pronoun, which is also a noun.
                """
        if self.contain_type('JJ') or self.contain_type('ADJP'):

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
                # adj before a noun

                for i in range(0, len(self._subtrees)):
                    # eg. He is a cool Canadian boy
                    # noun is not followed the adj or adjp(cool and young).
                    # eg. A [cool and young](adjp) boy/ a cool boy.
                    if i != len(self._subtrees) - 1 and \
                            (self._subtrees[i]._root['label'] == 'JJ' or
                             self._subtrees[i]._root['label'] == 'ADJP') \
                            and (self._subtrees[i + 1]._root['label'] == 'NN' or
                                 self._subtrees[i + 1]._root['label'] == 'NNS'):
                        if not whether_question:
                            return ''
                        else:
                            return 'it is a question sentence and difficult to determinate'

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

                for x in self._subtrees:
                    result = x.check_adj(whether_question)
                    if result != '':
                        return result

                return 'can not easily judge'

            elif self._root['label'] == 'VP':
                # adj must follow the verb because the first element in VP is verb
                if self._subtrees[0]._root['label'] == 'JJ':
                    # The man happy is.
                    return "adj in wrong position"

                if self._subtrees[1]._root['label'] == 'JJ' or \
                        self._subtrees[1]._root['label'] == 'ADJP' and \
                        self._subtrees[0]._root['text'] == 'am' or self._subtrees[0]._root[
                    'text'] == 'is' or self._subtrees[0]._root['text'] == 'are' or \
                        self._subtrees[0]._root['text'] == 'was' or \
                        self._subtrees[0]._root['text'] == 'were':
                    # eg. The man is cool.
                    if not whether_question:
                        return ''
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
        case2: swimming(vbg in constituent tree) man

         Warning: Swimming is good.('swimming' here is in noun class according
         to the constituent tree)
        """

        if self.contain_type('VBG'):
            if self._root['label'] == 'VBG':
                return 'it is hard to determinate'
            if self._root['label'] == 'SQ':
                # question sentence eg. is he swimming?
                # Is the swimming man cool?
                return 'This is a question sentence and hard to judge'
            if self._root['label'] == 'SBAR':
                for x in self._subtrees:
                    result = x.check_vbg()
                    if result != '':
                        return result
            if self._root['label'] == 'VP' and any(
                    x._root['label'] == 'VBG' for x in self._subtrees):
                # if VBG is in the subtree of VP

                if self._subtrees[0]._root['label'] == 'VBG':
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


he = GrammarTree('PRP', [], 'he')
plays = GrammarTree('VBZ', [], 'plays')
good = GrammarTree('word', [], 'good')
happy = GrammarTree('JJ', [], 'happy')
nn = GrammarTree('PRP', [he], '')
vbz = GrammarTree('VBZ', [plays], '')
adj = GrammarTree('JJ', [], '')

np = GrammarTree('NP', [nn], '')
adjp = GrammarTree('ADJP', [happy])
vp = GrammarTree('VP', [vbz, adjp], '')

beautiful = GrammarTree('JJ', [], 'good')
adjp1 = GrammarTree('ADJP', [beautiful])

s = GrammarTree('S', [np, vp])
# he plays happy (wrong eg)
root = GrammarTree('ROOT', [s])

vbz2 = GrammarTree('VBZ', [], 'sings')
vbz1 = GrammarTree('VBZ', [], 'is')

prp1 = GrammarTree('PRP', [], 'She')
np1 = GrammarTree('NP', [prp1])
vp1 = GrammarTree('VP', [vbz1])

advp = GrammarTree('ADVP', [beautiful])
sentence = GrammarTree('S', [np1, advp, vp1], '')
# She beautiful is (wrong eg)
s1 = GrammarTree('ROOT', [sentence])

s3 = GrammarTree('S', [np, adjp])
# he beautiful.(wrong eg)
root2 = GrammarTree('ROOT', [s3])

# The man who happy is Dim.(wrong)

the = GrammarTree('DT', [], 'The')
man = GrammarTree('NN', [], 'man')
np_1 = GrammarTree('NP', [the, man])
who = GrammarTree('WP', [], 'who')
whnp = GrammarTree('WHNP', [who])
frag = GrammarTree('FRAG', [adjp])
sbar = GrammarTree('SBAR', [whnp, frag])
np_2 = GrammarTree('NP', [np_1, sbar])
nnp = GrammarTree('NNP', [], 'Dim')
np_3 = GrammarTree('NP', [nnp])
vp_1 = GrammarTree('VP', [vbz1, np_3])
sentence_1 = GrammarTree('S', [np_2, vp_1])
root_1 = GrammarTree('ROOT', [sentence_1])

# The man who play happy is Dim. (wrong)
the2 = GrammarTree('DT', [], 'The')
man2 = GrammarTree('NN', [], 'man')
np_12 = GrammarTree('NP', [the2, man2])
who2 = GrammarTree('WP', [], 'who')
whnp2 = GrammarTree('WHNP', [who2])
vp_32 = GrammarTree('VP', [vbz, adjp])
s_12 = GrammarTree('S', [vp_32])
sbar2 = GrammarTree('S', [whnp, s_12])
np_22 = GrammarTree('NP', [np_12, sbar2])
nnp2 = GrammarTree('NNP', [], 'Dim')
np_32 = GrammarTree('NP', [nnp2])
vp_12 = GrammarTree('VP', [vbz1, np_32])
sentence_12 = GrammarTree('S', [np_22, vp_12])
root_3 = GrammarTree('ROOT', [sentence_12])

# Check check_vbg
# he is swimming
he = GrammarTree('PRP', [], 'he')
vbz1 = GrammarTree('VBZ', [], 'is')
nn = GrammarTree('PRP', [he], '')
np = GrammarTree('NP', [nn], '')
swimming = GrammarTree('VBG', [], 'swimming')
vp3 = GrammarTree('VP', [swimming])
vp4 = GrammarTree('VP', [vbz1, vp3])
sen = GrammarTree('S', [np, vp4])
root3 = GrammarTree('ROOT', [sen])

# he plays eating(wrong_)
vbz = GrammarTree('VBZ', [plays], '')
eating = GrammarTree('VBG', [], 'eating')
vp5 = GrammarTree('VP', [eating])
s4 = GrammarTree('S', [vp5])
vp6 = GrammarTree('VP', [vbz, s4])
s5 = GrammarTree('S', [np, vp6])
root4 = GrammarTree('ROOT', [s5])

# The man who eats eating.
eats = GrammarTree('VBZ', [], 'eats')
ting = GrammarTree('NNP', [], 'Ting')
np_11 = GrammarTree('NP', [the, man])
whnp = GrammarTree('WHNP', [who])
vp_11 = GrammarTree('VP', [eats, s4])
s_11 = GrammarTree('S', [vp_11])
sbar_11 = GrammarTree('SBAR', [whnp, s_11])
np_22 = GrammarTree('NP', [np_11, sbar_11])
root5 = GrammarTree('ROOT', [np_22])
