import pandas as pd
import re


def gujarati_pos_tagging(sentence):
    #Word Tokenization
    def WordTokenizer(data, keep_punctuations=False):
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

    #Sentence tokenization
    def SentenceTokenizer(data):
        data = data.strip()
        data = data.strip('\n')
        data = re.sub(r'([.!?])', r'\1 ', data)
        data = re.split(r'  ',data)
        return data

    data = pd.read_excel("C:/Users/vedan/Downloads/pos tagg vedant/POS Tagging-20230926T042149Z-001/POS Tagging/Gujarati_new_stopwords.xlsx")
    data.drop(columns=['Unnamed: 0'], inplace=True)

    #Sentence Tokenization
    tokenized_sentence = SentenceTokenizer(sentence)
    tokenized_sentence

    #Word Tokenization
    tokenized = [WordTokenizer(i) for i in tokenized_sentence]
    tokenized

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

        word_before = ''

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
                rules_applied_list[i] = [j]
                pos_tags[next_word_sentences[next_word+1]] = 'Verb'
                count = 0
                sent += 1
                rules_applied += 1
                rules_applied_list[i].append(pos_tags[i])

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
        
        if j == 'Adjective':
            if pos_tags[next_word_sentences[next_word+1]] == 'Missing':
                rules_applied_list[i] = [j]
                pos_tags[next_word_sentences[next_word+1]] = 'Noun'
                rules_applied_list[i].append(pos_tags[i])

        next_word += 1

    sentence = list(pos_tags.keys())
    final_tags = list(pos_tags.values())

    print(f'Rules Applied: - {rules_applied}\n')
    for i in range(len(sentence)):
        print(f'{sentence[i]}\t------▶\t{final_tags[i]}')

    print('\n\n')
    print("***** RULES APPLIED *****\n")
    for i,j in rules_applied_list.items():
        print(f'{i}\t----▶  {j[0]}\t----▶  {j[1]}')


sentence = 'મારો મિત્ર# @ ગમ્યો છે મહેનત થી વેદાંત!'

gujarati_pos_tagging(sentence=sentence)