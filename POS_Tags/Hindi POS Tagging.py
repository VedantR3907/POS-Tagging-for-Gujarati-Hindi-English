import nltk
from nltk.corpus import indian
from nltk.tag import tnt
train_data = indian.tagged_sents("hindi.pos")
tnt_pos_tagger = tnt.TnT()
tnt_pos_tagger.train(train_data)


def hindi_pos_tagging(text):
    words = (tnt_pos_tagger.tag(nltk.word_tokenize(text)))

    sentence = [i[0] for i in words]
    final_tags = [i[1] for i in words]
    final_tags = list(map(lambda x:x.replace('Unk', 'NN'), final_tags))

    for i in range(len(sentence)):
        print(f'{sentence[i]}\t------▶\t\t{final_tags[i]}')
