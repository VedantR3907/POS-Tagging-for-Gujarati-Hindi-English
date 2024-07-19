import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Tokenize the text into words

def english_pos_tagging(text):
    words = word_tokenize(text)

    # Perform POS tagging

    pos_tags = pos_tag(words)

    sentence = [i[0] for i in pos_tags]
    final_tags = [i[1] for i in pos_tags]

    for i in range(len(sentence)):
        print(f'{sentence[i]}\t------▶ {final_tags[i]}')
