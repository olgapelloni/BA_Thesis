# -*- coding: utf-8 -*-
import codecs
import re

# ------ PRE-EDITING ------

def assign(self):
    self.transcription = self.word.lower()

def jot_vowels_substitution(self):
    if self.transcription[0] in self.jot_vowels.keys():
        self.transcription = ''.join(u'j' + self.jot_vowels[self.transcription[0]] + self.transcription[1:])

    if self.transcription[-1] in self.jot_vowels.keys() and self.transcription[-2] not in self.all_cons:
        self.transcription = ''.join(self.transcription[:-1] + u'j' + self.jot_vowels[self.transcription[-1]])

    for i in range(1, len(self.transcription)):
        if self.transcription[i] in self.jot_vowels.keys():
            if self.transcription[i-1] in self.pairing_cons:
                self.transcription = ''.join(self.transcription[:i] + u'\'' + self.jot_vowels[self.transcription[i]] + self.transcription[i+1:])

            if self.transcription[i-1] in self.all_vowels or self.transcription[i-1] == u'̀':
                self.transcription = ''.join(self.transcription[:i] + u'j' + self.jot_vowels[self.transcription[i]] + self.transcription[i+1:])
            if self.transcription[i-1] in u'ьъ':
                self.transcription = ''.join(self.transcription[:i-1] + u'j' + self.jot_vowels[self.transcription[i]] + self.transcription[i+1:])

def cons_substitutions(self):
    self.transcription = self.transcription.replace(u'й', u'j')
    self.transcription = self.transcription.replace(u'ч', u'ч\'')
    self.transcription = self.transcription.replace(u'щ', u'ш\'')

    for i in range(1, len(self.transcription)):
        if self.transcription[i-1] in self.pairing_cons:
            if self.transcription[i] == u'ь':
                self.transcription = ''.join(self.transcription[:i] + u'\'' + self.transcription[i+1:])
            if self.transcription[i] in u'еи':
                self.transcription = ''.join(self.transcription[:i] + u'\'' + self.transcription[i:])

    if self.transcription[len(self.transcription)-1] == u'ь':
        if self.transcription[(len(self.transcription)-2)] in self.pairing_cons:
            self.transcription = ''.join(self.transcription[:len(self.transcription)-1] + u'\'')
        else:
            self.transcription = ''.join(self.transcription[:len(self.transcription)-1])

def delete_icts(self):
    icts = []
    self.transcription = self.transcription.replace(u'̀', u'`')
    for i in range(len(self.transcription)):
        if self.transcription[i] == u'`':
            icts.append(i)
    if len(icts) == 1:
        self.stress = icts[0]
    else:
        self.stress = icts[-1]
        for ict in reversed(icts[:-1]):
            self.transcription = ''.join(self.transcription[:ict] + self.transcription[ict+1:])
            self.stress -= 1

def yo_words_create(self):
    f = codecs.open('./yo_words.txt', 'r', 'utf-8')
    word = re.compile(u'^[а-яё]+')
    for line in f:
        find_word = re.search(word, line)
        if find_word != None:
            self.yo_words.append(find_word.group(0))

def yo_replace(self):
    if u'ѐ'in self.transcription:
        possible_yo_word = self.transcription
        possible_yo_word = possible_yo_word.replace(u'ѐ', u'ё')
        possible_yo_word = possible_yo_word.replace(u'̀', u'')
        for word in self.yo_words:
            if possible_yo_word == word:
                self.transcription = word
                self.transcription = self.transcription.replace(u'ё', u'ё̀')


# ------ VOWELS ------

def apply_reductions(self):
        self.pre_vowels = []
        for i in range(self.stress - 1):
            if self.transcription[i] in self.all_vowels:
                self.pre_vowels.append(i)
        if len(self.pre_vowels) >= 1:
            self.apply_first_reduction = True
        if len(self.pre_vowels) >= 2:
            self.apply_other_pre_reduction = True
        for i in range(self.stress, len(self.transcription)):
            if self.transcription[i] in self.all_vowels:
                self.apply_post_reduction = True
                break


def after_hard_hushing(self):
    for cons in self.hard_hushing_cons:
        self.transcription = self.transcription.replace(cons + u'и', cons + u'ы')
        self.transcription = self.transcription.replace(cons + u'ь', cons + u'ъ')
        self.transcription = self.transcription.replace(cons + u'jъ', cons + u'ъ')

def post_reduction(self):
    for i in range(self.stress, len(self.transcription)):
        if (self.transcription[i] == u'а' or self.transcription[i] == u'о') and (self.transcription[i-1] != u'\'' and self.transcription[i-1] != u'j') or \
                (self.transcription[i-2] in self.hard_hushing_cons and self.transcription[i] == u'е'):
            self.transcription = ''.join(self.transcription[:i] + u'ъ' + self.transcription[i+1:])

        if self.transcription[i] == u'я' or self.transcription[i] == u'е' or \
                ((self.transcription[i-1] == u'\'' or self.transcription[i-1] == u'j') and self.transcription[i] == u'а'):
            self.transcription = ''.join(self.transcription[:i] + u'ь' + self.transcription[i+1:])

def first_pre_stress_reduction(self):
    first_pre_vowel = self.pre_vowels[-1]
    if self.transcription[first_pre_vowel] == u'о':
        self.transcription = ''.join(self.transcription[:first_pre_vowel] + u'а' + self.transcription[first_pre_vowel+1:])
    elif self.transcription[first_pre_vowel] == u'е' or self.transcription[first_pre_vowel] == u'я' or \
            ((self.transcription[first_pre_vowel - 1] == u'\'' or self.transcription[first_pre_vowel - 1] == u'j')
             and (self.transcription[first_pre_vowel] == u'а' or self.transcription[first_pre_vowel] == u'е')):
        self.transcription = ''.join(self.transcription[:first_pre_vowel] + u'и' + self.transcription[first_pre_vowel+1:])

def other_pre_stress_reduction(self):
    i = 0
    while i < len(self.pre_vowels) - 1:
        start = i
        cur_pre_vowel = self.pre_vowels[i]
        if cur_pre_vowel == 0:
            if self.transcription[cur_pre_vowel] == u'о':
                self.transcription = ''.join(u'а' + self.transcription[cur_pre_vowel+1:])
        else:

            if self.transcription[cur_pre_vowel] == u'а' and self.transcription[cur_pre_vowel - 1] != u'j' or self.transcription[cur_pre_vowel] == u'о' or \
                   (self.transcription[cur_pre_vowel] == u'е' and self.transcription[cur_pre_vowel - 1] in self.hard_hushing_cons):
                    self.transcription = ''.join(self.transcription[:cur_pre_vowel] + u'ъ' + self.transcription[cur_pre_vowel+1:])

            if self.transcription[cur_pre_vowel] == u'е' or self.transcription[cur_pre_vowel] == u'я' or \
                   (self.transcription[cur_pre_vowel] == u'а' and (self.transcription[cur_pre_vowel - 1] in self.soft_hushing_cons or
                                                                           self.transcription[cur_pre_vowel - 1] == u'j')):
                    self.transcription = ''.join(self.transcription[:cur_pre_vowel] + u'ь' + self.transcription[cur_pre_vowel+1:])


        if i == start:
            i += 1

def hiatus(self):
    for i in range(len(self.transcription[:self.stress])):
        if (self.transcription[i] == u'а' and (self.transcription[i+1] == u'а' or self.transcription[i+1] == u'о')) or (self.transcription[i] == u'о' and (self.transcription[i+1] == u'а' or self.transcription[i+1] == u'о')):
            self.transcription = ''.join(self.transcription[:i] + u'АА' + self.transcription[i+2:])

        if self.transcription[i] == u'е':
            if self.transcription[i+1] == u'е':
                self.transcription = ''.join(self.transcription[:i] + u'ьjь' + self.transcription[i+2:])
            if self.transcription[i+1] == u'а' or self.transcription[i+1] == u'о':
                self.transcription = ''.join(self.transcription[:i+1] + u'А' + self.transcription[i+2:])



# ------ CONSONANTS ------

def voiceless(self):
    exceptions = [u'бо`г', u'го`споди']
    for cons in self.voiced_cons.keys():
        if self.transcription not in exceptions:
            if self.transcription.endswith(cons):
                self.transcription = ''.join(self.transcription[:-1] + self.voiced_cons[self.transcription[-1]])
        else:
            self.transcription = self.transcription.replace(u'г', u'х')  # No difference here between γ and х

def simplification(self):
    self.transcription = self.transcription.replace(u'нтск', u'нск')
    self.transcription = self.transcription.replace(u'ндск', u'нск')
    self.transcription = self.transcription.replace(u'стц', u'ц')
    self.transcription = self.transcription.replace(u'здц', u'ц')
    self.transcription = self.transcription.replace(u'здч', u'ш\':')
    self.transcription = self.transcription.replace(u'здн', u'зн')
    self.transcription = self.transcription.replace(u'стс', u'с:')
    self.transcription = self.transcription.replace(u'ндц', u'нц')
    self.transcription = self.transcription.replace(u'рдц', u'рц')
    self.transcription = self.transcription.replace(u'рдч', u'рч')
    self.transcription = self.transcription.replace(u'лнц', u'нц')
    self.transcription = self.transcription.replace(u'ргск', u'рск')
    self.transcription = self.transcription.replace(u'ркск', u'рск')
    self.transcription = self.transcription.replace(u'скск', u'с:к')
    self.transcription = self.transcription.replace(u'стск', u'с:к')
    self.transcription = self.transcription.replace(u'тств', u'цств')
    self.transcription = self.transcription.replace(u'дств', u'цств')
    self.transcription = self.transcription.replace(u'тс', u'ц')
    self.transcription = self.transcription.replace(u'тс\'', u'ц')
    self.transcription = self.transcription.replace(u'дц', u'ц')
    self.transcription = self.transcription.replace(u'дш\'', u'ч\'ш\'')
    self.transcription = self.transcription.replace(u'тш\'', u'ш\'')
    self.transcription = self.transcription.replace(u'сч\'', u'ш\'')
    self.transcription = self.transcription.replace(u'гк', u'хк')
    self.transcription = self.transcription.replace(u'зж', u'ж')
    self.transcription = self.transcription.replace(u'сш', u'ш')
    self.transcription = self.transcription.replace(u'дш\'', u'ч\'ш\'')
    self.transcription = self.transcription.replace(u'дч\'', u'ч\'')
    if not self.transcription.startswith(u'отчеств'):
        self.transcription = self.transcription.replace(u'тч\'', u'ч\'')
    if u'чу`вств' or u'здра`вств' in self.transcription:
        self.transcription = self.transcription.replace(u'вств', u'ств')
    if u'что`' in self.transcription:
        self.transcription = self.transcription.replace(u'чт', u'шт')

    #self.transcription = self.transcription.replace(u'стн', u'сн') only in some words
    #стл also in some words
    #стс
    # ндш, ндж, нтш

def assimilation(self):
    for i in range(len(self.transcription)-1):

        # Make voiceless
        if self.transcription[i] in self.voiced_cons.keys():
            if self.transcription[i+1] in self.voiced_cons.values() or self.transcription[i+1] in u'хцч':
                self.transcription = ''.join(self.transcription[:i] + self.voiced_cons[self.transcription[i]] + self.transcription[i+1:])

        # Make voiced
        if self.transcription[i] in self.voiced_cons.values():
            if self.transcription[i+1] in u'бгджз':
                replacement = [key for key, value in self.voiced_cons.iteritems() if value == self.transcription[i]][0]
                self.transcription = ''.join(self.transcription[:i] + replacement + self.transcription[i+1:])


def orfo_check(self):
    for shn_word in self.shn_words:
        if self.transcription.startswith(shn_word):
            self.transcription = self.transcription.replace(u'чн', u'шн')

    possible_orfo_word = self.transcription
    possible_orfo_word = possible_orfo_word.replace(u'̀', u'')

    for word in self.hard_de_words:
        if possible_orfo_word.startswith(word):
            self.transcription = self.transcription.replace(u'де', u'дэ')
            self.transcription = self.transcription.replace(u'дѐ', u'дэ̀')
    for word in self.hard_te_words:
        if possible_orfo_word.startswith(word):
            self.transcription = self.transcription.replace(u'те', u'тэ')
            self.transcription = self.transcription.replace(u'тѐ', u'тэ̀')
    for word in self.hard_ze_words:
        if possible_orfo_word.startswith(word):
            self.transcription = self.transcription.replace(u'зе', u'зэ')
            self.transcription = self.transcription.replace(u'зѐ', u'зэ̀')
    for word in self.hard_se_words:
        if possible_orfo_word.startswith(word):
            self.transcription = self.transcription.replace(u'се', u'сэ')
            self.transcription = self.transcription.replace(u'сѐ', u'сэ̀')
    for word in self.hard_re_words:
        if possible_orfo_word.startswith(word):
            self.transcription = self.transcription.replace(u'ре', u'рэ')
            self.transcription = self.transcription.replace(u'рѐ', u'рэ̀')
    for word in self.hard_ne_words:
        if possible_orfo_word.startswith(word):
            self.transcription = self.transcription.replace(u'не', u'нэ')
            self.transcription = self.transcription.replace(u'нѐ', u'нэ̀')
    for word in self.hard_pe_words:
        if possible_orfo_word.startswith(word):
            self.transcription = self.transcription.replace(u'пе', u'пэ')
            self.transcription = self.transcription.replace(u'пѐ', u'пэ̀')
    for word in self.hard_fe_words:
        if possible_orfo_word.startswith(word):
            self.transcription = self.transcription.replace(u'фе', u'фэ')
            self.transcription = self.transcription.replace(u'фѐ', u'фэ̀')



