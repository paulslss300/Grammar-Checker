"""
This file only contains four grammar checking methods.
The classes we need will be stored in GrammarTree.py. I will import that file first.
"""


def plural_nouns_match_singular_verb(self) -> str:
    """
    This method test if sentence match singular form of verbs to plural form of nouns.
    For some complex or hard-to-determine situation, it just returns hard to determine.
    This method can be called individually or as a helper function.
    This method can NOT detect a sentence starts with pronoun.
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
    for subtree in self._subtrees:
        if subtree._root['label'] == 'S':
            if subtree.plural_nouns_match_singular_verb() == result_mistake:
                return result_mistake
    return 'Maybe it is correct or it is hard to determine.'


def singular_noun_match_plural_verb(self) -> str:
    """
    This method check whether a sentence mistakenly matches singular noun to plural verb.
    For some complex or hard-to-determine situation, it just returns hard to determine.
    This method can be called individually or as a helper function.
    This method can NOT detect a sentence starts with pronoun.
    """
    # if self._root['label'] == 'S':
    #     s = self
    #     first = s._subtrees[0]._subtrees[0]
    #     if first._root['label'] == 'PRP':
    #         return 'This method can not detect a sentence starts with pronoun.'
    first = self
    while first._subtrees != []:
        first = first._subtrees[0]
    if first._root['label'] == 'PRP':
        return 'The subject is pronoun. This method can not determine.'
    result_mistake = 'This sentence may mistakenly match plural verb to singular nouns.'
    # Exist singular Noun. No and. No plural nouns.
    # Exist verb phrase. Exist third singular verb.
    if self.contain_type('NN') and not self.contain_type('NNS') and not \
            self.contain_type('CC') and self.contain_type('VP') \
            and not self.contain_type('VBD') and not self.contain_type('VBZ'):
        return result_mistake
    # Only check sentence and sub-sentence.
    for s in self._subtrees:
        if s._root['label'] == 'S':
            if s.singular_noun_match_plural_verb() == result_mistake:
                return result_mistake
    return 'Maybe it is correct or it is hard to determine.'


def check_noun_plural_and_singular(self) -> str:
    """
    This method will call two helper methods above.
    This method checks whether a singular/plural noun mistakenly matches plural/singular verbs.
    This method can NOT detect a sentence starts with pronoun.
    """
    result_so_far = set()
    result_so_far.add(self.singular_noun_match_plural_verb())
    result_so_far.add(self.plural_nouns_match_singular_verb())
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


def check_end_punctuations(self) -> str:
    """
    Check whether the last punctuation in the sentence is correct.
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


def existence_of_noun(self) -> str:
    """
    This method check whether this sentence have a noun (phrase).
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


def multiple_verbs_in_one_simple_sentence(self) -> str:
    """
    This method detect whether a simple (combining) sentence contains more than one verb.
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
                for i in l_copy:
                    if i._root['label'] in vb_use_set:
                        return result_a
    return 'No such kind of mistakes have been detected, yet.'
