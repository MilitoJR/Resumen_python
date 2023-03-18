import urllib.request
import re
import nltk
from inscriptis import get_text

#Scrapea articulo de wikipedia
text = "The world economy or global economy is the economy of all humans of the world, referring to the global economic system, which includes all economic activities which are conducted both within and between nations, including production, consumption, economic management, work in general, exchange of financial values and trade of goods and services"
#html = urllib.request.urlopen(text).read().decode('utf8')
#text = get_text(html)
article_text = text.replace("[ edit ]", "")

from nltk import word_tokenize, sent_tokenize
#nltk.download()
#Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

#nltk.download()
#En esta parte hace la tokenizacion
sentence_list = nltk.sent_tokenize(article_text)

#En esta parte encuentra la frecuencia de las palabras
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

#
maximum_frequncy = max (word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word]=(word_frequencies[word]/maximum_frequncy)

#Calcula las frases que mas se repiten
sentences_socores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 100:
                if sent not in sentences_socores.keys():
                    sentences_socores[sent] = word_frequencies[word]
                else:
                    sentences_socores[sent] += word_frequencies[word]

#Realiza el resumen con las mejores frases
import heapq
summary_sentences = heapq.nlargest(7, sentences_socores, key=sentences_socores.get)

summary = ' '.join(summary_sentences)
#print(summary)
#from nltk.corpus import treebank
#t = treebank.parsed_sents('wsj_0001.mrg')[0]
#t.draw()


from googletrans import Translator
translator = Translator() 
textTraslate= translator.translate(summary, src='en', dest='es')
print(textTraslate.text)




from gtts import gTTS

import os
mytext = textTraslate.text
languaje = 'es'
myobj = gTTS (text= textTraslate.text, lang=languaje, slow=False)
myobj.save("word.mp3")
os.system("word.mp3")

