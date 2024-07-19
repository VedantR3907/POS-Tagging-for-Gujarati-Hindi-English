with open("C:/Users/vedan/Downloads/text.txt", 'r') as file:
    s = file.read()
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
s = s.split(' ')
t,temp = [], 0
for i,j in enumerate(s):
    if (j[-1] == '.') and (len(j[:-1])>2) and ('.' not in j[:-1]) and (j[:-1] not in stop_words):
        t.append(' '.join(s[temp:i+1]))
        temp = i+1
    elif (j[-1] == '.') and (len(j[:-1])>2) and ('.' in j[:-1]) and (j[:-1] not in stop_words):
        if i<len(s)-1:
            if s[i+1][0].isupper():
                t.append(' '.join(s[temp:i+1]))
                temp = i+1
    if i >= len(s)-1:
        t.append(' '.join(s[temp:i+1]))

print("\n","*"*50, "Sentences: - ", "*"*50,"\n")
for i,j in enumerate(t[:-1]):
    print(f'{i+1}. {j}\n')