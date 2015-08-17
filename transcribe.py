# -*- coding: utf-8 -*-

# Transform word into transcription
# Rules from http://fonetica.philol.msu.ru/

import pre_editing

class Transcription():
    def __init__(self):
        self.all_vowels = [u'а', u'о', u'у', u'э', u'ы', u'и', u'е', u'ю', u'я']
        self.jot_vowels = {u'ю': u'у', u'я': u'а', u'е': u'е', u'ё': u'о'}
        self.all_cons = [u'б', u'в', u'г', u'д', u'ж', u'з', u'й', u'к', u'л', u'м', u'н', u'п',
                         u'р', u'с', u'т', u'ф', u'х', u'ц', u'ш', u'щ', u'ч']
        self.voiced_cons = {u'б': u'п', u'в': u'ф', u'г': u'к', u'д': u'т', u'ж': u'ш', u'з': u'с'}
        self.pairing_cons = [u'б', u'в', u'г', u'д', u'з', u'к', u'л', u'м', u'н', u'п',
                             u'р', u'с', u'т', u'ф', u'х']
        self.hard_hushing_cons = [u'ш', u'ж', u'ц']
        self.soft_hushing_cons = [u'ч', u'щ']
        self.apply_first_reduction = False
        self.apply_other_pre_reduction = False
        self.apply_post_reduction = False
        self.yo_words = []
        self.shn_words = [u'конечно', u'скучн', u'нарочн', u'яичниц,'
                          u'прачечн', u'скворечн', u'девичн', u'горчичн']  # better to have bigger list
        self.hard_de_words = [u'декольте', u'дельта', u'дендрари', u'дефиле',
                             u'детектор', u'детектив', u'диадема', u'тенденци',
                             u'цитадель',  u'шедевр',  u'рандеву', u'денди']
        self.hard_te_words = [u'антитез',  u'тезис',  u'гротеск',  u'интенсив',
                              u'метрополитен', u'патети', u'бутерброд',  u'контейнер',
                              u'теннис',  u'пастель',  u'синтети',  u'альтерна',
                              u'сентенци',  u'тенденци', u'коктейл',  u'штепсел',
                              u'компьютер', u'кортеж', u'ателье', u'свитер',
                              u'пастеризован', u'принтер', u'лотере', u'эстет',
                              u'претен', u'протекци', u'интер', u'тент']
        self.hard_ze_words = [u'безе', u'зеро', u'кузен', u'морзе', u'экзем']
        self.hard_se_words = [u'антисепт', u'диспансер',  u'нонсенс',  u'сенсор',
                              u'плиссе',  u'фрикасе', u'эссе']
        self.hard_re_words = [u'регби',  u'реквием',  u'кабаре',  u'пюре',  u'тире']
        self.hard_ne_words = [u'бизнес', u'генез', u'анестези', u'генет',
                              u'майонез', u'полонез', u'тоннел', u'пенсне', u'энерги']
        self.hard_pe_words = [u'капелл']
        self.hard_fe_words = [u'галифе', u'кафе']
        self.pre_vowels = []
        self.word_vowels = []
        self.word_consonants = []
        self.stress = 0
        self.word = ''
        self.transcription = ''

    def pre(self, flag):
        pre_editing.assign(self)
        pre_editing.yo_words_create(self)
        pre_editing.orfo_check(self) #-- becomes very slowly
        if flag == 1:
            pre_editing.yo_replace(self)
        pre_editing.assimilation(self)
        pre_editing.cons_substitutions(self)
        pre_editing.jot_vowels_substitution(self)
        pre_editing.delete_icts(self)

    def vowels(self):
        pre_editing.apply_reductions(self)
        #pre_editing.hiatus(self) -- often works not correctly
        if self.apply_other_pre_reduction:
            pre_editing.other_pre_stress_reduction(self)
        if self.apply_first_reduction:
            pre_editing.first_pre_stress_reduction(self)
        if self.apply_post_reduction:
            pre_editing.post_reduction(self)
        self.transcription = self.transcription.lower()
        pre_editing.after_hard_hushing(self)
        for i in range(len(self.transcription)-1):
            if self.transcription[i] in self.pairing_cons and self.transcription[i+1] == u'ь':
                 self.transcription = ''.join(self.transcription[:i+1] + u'\'' + self.transcription[i+1:])

    def consonants(self):
        pre_editing.voiceless(self)
        pre_editing.simplification(self)

    def transform(self, flag):
        self.pre(flag)
        self.vowels()
        self.consonants()
        if u'ё' in self.transcription:
            self.transcription = self.transcription.replace(u'ё', u'о')
        for sound in self.transcription:
            if sound in self.all_cons or sound == u'j':
                self.word_consonants.append(sound)
            if sound in self.all_vowels or sound in u'ьъ':
                self.word_vowels.append(sound)


# word1 = u'сла̀ве'
# t = Transcription()
# t.word = word1
# t.transform(1)
# print t.word
# print t.transcription


