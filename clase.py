import urllib.request
import re
import nltk
from inscriptis import get_text

#Scrapea articulo de wikipedia
text = "The Nissan Skyline GT-R (Japanese: 日産・スカイラインGT-R, Hepburn: Nissan Sukairain GT-R) is a sports car based on the Nissan Skyline range. The first cars named Skyline GT-Rwere produced between 1969 and 1972 under the model code KPGC10, and were successful in Japanese touring car racing events. This model was followed by a brief production run of second-generation cars, under model code KPGC110, in 1973.After a 16-year hiatus, the GT-R name was revived in 1989 as the BNR32 (R34) Skyline GT-R. Group A specification versions of the R32 GT-R were used to win the Japanese Touring Car Championship for four years in a row. The R32 GT-R also had success in the Australian Touring Car Championship, with Jim Richards using it to win the championship in 1991 and Mark Skaife doing the same in 1992, until a regulation change excluded the GT-R in 1993. The technology and performance of the R32 GT-R"
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
mytext = text
languaje = 'en'
myobj = gTTS (text=mytext, lang=languaje, slow=False)
myobj.save("nissan.mp3")
os.system("nissan.mp3")