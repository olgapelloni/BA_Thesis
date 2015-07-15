# -*- coding: utf-8 -*-

import codecs
import os
from lxml import etree
from transcribe import Transcription

# Walk through each document
# Inside document: go inside a verse; find rhymes inside; write down path-verse-word pair

# TO DO:
# 1. Rich rhyme when it's after soft consonant +
# 2. Degree of exactness + and degree of richness
# 3. Word class and word form
# 4. Try out Neo4j +

class Rhymes:
    def __init__(self):
        self.root_name = ''
        self.result_table = ''
        self.rhymes = ''

    # Transform into transcription
    def transcribe(self, word):
        t = Transcription()
        t.word = word
        t.transform()
        return t

    def analyse(self):
        self.rhymes = codecs.open(self.result_table, 'w', 'utf-8')
        self.rhymes.write('file,verse,word1,word2,stress_position,exactness,degree_exactness,richness,dissonance\n')

        for root, dirs, files in os.walk(self.root_name):

            # Go into each document
            for name in files:
                print os.path.abspath(os.path.join(root, name))
                path = os.path.abspath(os.path.join(root, name))

                f = codecs.open(path, 'r', 'cp1251')
                text = f.read().encode('utf-8')
                f.close()

                # Parse the document
                tree_root = etree.XML(text, etree.HTMLParser())
                counter = 0
                for d in tree_root.iter():

                    cur_rhymes = []

                    # Inside each verse
                    if d.tag == 'p' and 'class' in d.attrib and d.attrib['class'] == 'verse':
                        for child in d.iterchildren():
                            if child.tag == 'rhyme-zone':
                                if child.tail is not None:

                                    # Word in a rhyme position
                                    if child.tail is not None:
                                        word = child.tail.strip(u'.…,«»?)]}!:;,- ')
                                        cur_rhymes.append(word)

                        # Find rhymes
                        for i in range(len(cur_rhymes)-1):
                            for j in range(i, len(cur_rhymes)):
                                if i != j:
                                    trans1 = self.transcribe(cur_rhymes[i])
                                    trans2 = self.transcribe(cur_rhymes[j])
                                    stress1 = trans1.transcription.index('`')
                                    stress2 = trans2.transcription.index('`')

                                    new_record = ''

                                    # Rhymes with the same stressed vowel
                                    if trans1.transcription[stress1-1] == trans2.transcription[stress2-1]:
                                        new_record = name + ',' + str(counter) + ',' + cur_rhymes[i].lower() + ',' + cur_rhymes[j].lower()

                                        vowels1_after = 0
                                        for sound in trans1.transcription[stress1+1:len(trans1.transcription)]:
                                            if sound in trans1.all_vowels or sound in u'ьъ':
                                                vowels1_after += 1

                                        vowels2_after = 0
                                        for sound in trans2.transcription[stress2+1:len(trans2.transcription)]:
                                            if sound in trans2.all_vowels or sound in u'ьъ':
                                                vowels2_after += 1

                                        # ----POSITION----
                                        # Male
                                        if vowels1_after == 0 and vowels2_after == 0:
                                            new_record += ',male'

                                        # Female
                                        elif vowels1_after == 1 and vowels2_after == 1:
                                            new_record += ',female'

                                        # Dactyl
                                        elif vowels1_after == 2 and vowels2_after == 2:
                                            new_record += ',dactyl'

                                        # Hyperdactyl
                                        elif vowels1_after >= 3 and vowels2_after >= 3:
                                            new_record += ',hyperdactyl'

                                        else:
                                            new_record += ',-'

                                        #----EXACTNESS----
                                        # Sounds after stress are the same
                                        exactness = 0
                                        min_len = min(len(trans1.transcription[stress1+1:]), len(trans2.transcription[stress2+1:]))
                                        k = 1
                                        while k <= min_len:
                                            if trans1.transcription[stress1+k] == trans2.transcription[stress2+k]:
                                                exactness += 1
                                            k += 1

                                        if k - exactness <= 1:
                                            res_exact = 'exact'
                                        else:
                                            res_exact = 'inexact'

                                        new_record += ',' + res_exact + ',' + str(k - exactness)

                                        #----RICHNESS----
                                        # Common sound before stress + the same sounds after
                                        if res_exact == 'exact':
                                            if trans1.transcription[stress1-2] == trans2.transcription[stress2-2]:
                                                if trans1.transcription[stress1-2] != '\'':
                                                    new_record += ',rich,-'
                                                else:
                                                    if trans1.transcription[stress1-3] == trans2.transcription[stress2-3]:
                                                        new_record += ',rich,-'
                                                    else:
                                                        new_record += ',poor,-'
                                            else:
                                                new_record += ',poor,-'
                                        else:
                                            new_record += ',poor,-'

                                    # Dissonance rhyme
                                    else:
                                        if len(trans1.transcription) == len(trans2.transcription):
                                            if trans1.transcription[:stress1-1] == trans2.transcription[:stress2-1] and trans1.transcription[stress1+1:] == trans2.transcription[stress2+1]:
                                                new_record = name + ',' + str(counter) + ',' + cur_rhymes[i].lower() + ',' + cur_rhymes[j].lower() + ',-\t-\t-\tDissonance'


                                    if new_record != '':
                                        print new_record.replace(',', '\t')
                                        new_record += '\n'
                                        self.rhymes.write(new_record)

                        counter += 1

rhymes = Rhymes()
rhymes.root_name = '.\poetic_corpus_tillXX\poetic\\texts\\xx\\sologub'
rhymes.result_table = 'result.csv'
rhymes.analyse()
