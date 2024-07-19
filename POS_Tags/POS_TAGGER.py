import pandas as pd
import nltk
nltk.download('indian')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import indian
from nltk.tag import tnt
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
train_data = indian.tagged_sents("hindi.pos")
tnt_pos_tagger = tnt.TnT()
tnt_pos_tagger.train(train_data)
import re
from langdetect import  detect

data = pd.read_excel("E:/Extra Codes/POS Tagging/datasets/Gujarati_new_stopwords.xlsx")
data.drop(columns=['Unnamed: 0'], inplace=True)


class POS_Tagger():
    ######################################################################################
    def __init__(self, Text, Mixed = False):
        self.Text = Text
        self.Mixed = Mixed
    ######################################################################################
    '''For Gujarati Language'''
    def WordTokenizer(self, data, keep_punctuations=False):
        if not keep_punctuations:
            data = re.sub(r'[.?/,:;*\"!+$#@%^&~\(\)]','',data)

        data = re.sub(r'([.,\'\\"!?%#@*<>|\+\-\(\)])', r' \1', data)
        data = re.sub(r'[।।(૧૨૩૪૫૬૭૮૯)*।।]', '  ', data)
        data = re.sub(r'[।।(123456789)*।।]', '  ', data)
        data = re.sub(r"   ", '', data)
        data = re.sub(r'…', " ", data)
        data = re.split(r'[ -]',data)
        return_list = []

        for i in data:
            if i:
                return_list.append(i)
                
        return return_list 
    ######################################################################################
    '''For Gujarati Language'''
    def SentenceTokenizer(self, data):
        data = data.strip()
        data = data.strip('\n')
        data = re.sub(r'([.!?])', r'\1 ', data)
        data = re.split(r'  ',data)
        return data
    ######################################################################################
    def English_POS_Tagger(self):
        words = word_tokenize(self.Text)

        pos_tags = pos_tag(words)

        sentence = [i[0] for i in pos_tags if i[0].isalpha() == True]
        final_tags = [i[1] for i in pos_tags if i[0].isalpha() == True]

        for i in range(len(sentence)):
            print(f'{sentence[i]}\t------▶ {final_tags[i]}')
    ######################################################################################
    def Hindi_POS_Tagger(self):
        words = (tnt_pos_tagger.tag(nltk.word_tokenize(self.Text)))

        sentence = [i[0] for i in words]
        final_tags = [i[1] for i in words]
        final_tags = list(map(lambda x:x.replace('Unk', 'NN'), final_tags))

        for i in range(len(sentence)):
            print(f'{sentence[i]}\t------▶\t{final_tags[i]}')
    ######################################################################################    
    def Gujarati_POS_Tagger(self):
        ######################################################################################
        #Sentence Tokenization
        tokenized_sentence = self.SentenceTokenizer(self.Text)
        tokenized_sentence

        #Word Tokenization
        tokenized = [self.WordTokenizer(i) for i in tokenized_sentence]
        tokenized
        ######################################################################################
        #Creating Dictonary for gujarati words with there respective pos tags from the dataset

        pos_tags = dict()
        tags_list = [[] for i in range(len(tokenized))]
        count = 0
        for i in tokenized:
            for j in i:
                if j in data['Gujarati_Tokens'].values and j not in pos_tags:
                    tag = data.loc[data['Gujarati_Tokens'] ==j, 'Tags'].values[0]
                    pos_tags[j] = tag
                    tags_list[count].append(tag)
                else:
                    if j not in data['Gujarati_Tokens'].values:
                        pos_tags[j] = 'Missing'
                        tags_list[count].append('Unknown')
            count += 1

            next_word_sentences = list(pos_tags.keys())
            next_word_tags = list(pos_tags.values())
        #####################################################################################
        #Rules for POS Tagging

        sentences_lens = [len(i) for i in tags_list]
        rules_applied_list = {} 
        count,sent,next_word,rules_applied = 0,0,0,0
        for i,j in pos_tags.items():
            count += 1
            if i[-2:] == 'યો' or i[-2:] == 'યુ' or i[-4:] == 'ય ું':
                rules_applied_list[i] = [j]
                pos_tags[i] = 'Verb'
                rules_applied += 1
                rules_applied_list[i].append(pos_tags[i])

            if i[-4:] == 'વ ું' or i[-4:] == 'વ ુ':
                rules_applied_list[i] = [j]
                pos_tags[i] = 'Verb'
                rules_applied += 1
                rules_applied_list[i].append(pos_tags[i])

            if i[-2:] == "ીશ" or i[-4:] == 'ીશું' or i[-2:] == 'શે':
                if count == sentences_lens[sent]:
                    rules_applied_list[i] = [j]
                    pos_tags[i] = 'Verb'
                    count = 0
                    sent += 1
                    rules_applied += 1
                    rules_applied_list[i].append(pos_tags[i])

            if i[-4:] == 'વાયો':
                rules_applied_list[i] = [j]
                pos_tags[i] = 'Verb'
                rules_applied += 1
                rules_applied_list[i].append(pos_tags[i])

            if i == 'નથી' or i == 'ને' or i == 'ન' or i == 'ના':
                if count != sentences_lens[sent]:
                    rules_applied_list[next_word_sentences[next_word+1]] = [next_word_tags[next_word+1]]
                    pos_tags[next_word_sentences[next_word+1]] = 'Verb'
                    count = 0
                    sent += 1
                    rules_applied += 1
                    rules_applied_list[next_word_sentences[next_word+1]].append('Verb')


            if i[-2:] == 'થી' or i[-2:] == 'તમ' or i[-2:] == 'માું':
                rules_applied_list[i] = [j]
                pos_tags[i] = 'Adverb'
                rules_applied += 1
                rules_applied_list[i].append(pos_tags[i])

            if i[:] == 'આ' or i[:] == 'એક':
                rules_applied_list[i] = [j]
                pos_tags[i] = 'Determiner'
                rules_applied += 1
                rules_applied_list[i].append(pos_tags[i])

            if i[:]=='!' or i[:]=='?' or i[:]==',' or i[:]=='.' or i[:]=='' or i[:]=='""' or i[:]==';' or i[:]==':' or i[:]==' '' ' or i[:]=='-':
                rules_applied_list[i] = [j]
                pos_tags[i] = 'Punctuations'
                rules_applied += 1
                rules_applied_list[i].append(pos_tags[i])
            
            # if j == 'Adjective':
            #     if pos_tags[next_word_sentences[next_word+1]] == 'Missing':
            #         rules_applied_list[next_word_sentences[next_word+1]] = [next_word_tags[next_word+1]]
            #         pos_tags[next_word_sentences[next_word+1]] = 'Noun'
            #         rules_applied_list[next_word_sentences[next_word+1]].append('Noun')

            next_word += 1
        ######################################################################################

        sentence = list(pos_tags.keys())
        final_tags = list(pos_tags.values())

        for i in range(len(sentence)):
            print(f'{sentence[i]}\t------▶\t{final_tags[i]}')

        if self.Mixed == False:
            print('\n\n')
            print(f'Rules Applied: - {rules_applied}\n')
            print("***** RULES APPLIED *****\n")
            for i,j in rules_applied_list.items():
                print(f'{i}\t----▶  {j[0]}\t----▶  {j[1]}')
        ######################################################################################

    ######################################################################################    
    def POS_Tags(self):
        if self.Mixed == True:
            temp = self.Text.split(' ')
            for i in temp:
                language = detect(i)
                self.Text = i
                if language == 'hi' or language == 'mr':
                    self.Hindi_POS_Tagger()
                elif language == 'gu':
                    self.Gujarati_POS_Tagger()
                else:
                    self.English_POS_Tagger()
        else:
            language = detect(self.Text)

            if language == 'hi':
                self.Hindi_POS_Tagger()
            elif language == 'gu':
                self.Gujarati_POS_Tagger()
            else:
                self.English_POS_Tagger()
        
    ######################################################################################
