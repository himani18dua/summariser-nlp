import urllib.request
import bs4 as BeautifulSoup
import nltk
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

text=urllib.request.urlopen("https://en.wikipedia.org/wiki/Machine_learning")
article=text.read()
article_parsed=BeautifulSoup.BeautifulSoup(article,'html.parser')
paras=article_parsed.find_all('p')
article_content=''
for p in paras:
    article_content+=p.text
stop_words=stopwords.words('english')
punctuation=punctuation +'\n'
word_freq={}
tokens=word_tokenize(article_content)
for word in tokens:
    if word.lower() not in stop_words:
        if word.lower() not in punctuation:
            if word not in word_freq.keys():
                word_freq[word]=1
            else:
                word_freq[word]+=1

max_freq=max(word_freq.values())
for word in word_freq.keys():
    word_freq[word]=word_freq[word]/max_freq
sentence=sent_tokenize(article_content)
sent_weight=dict() 
for s in sentence:
    sent_wc=len(word_tokenize(s))
    sent_wc_wo=0
    for ww in word_freq:
        if ww in s.lower():
            sent_wc_wo+=1
            if s in sent_weight:
                sent_weight[s]+=word_freq[ww]
            else:
                sent_weight[s]=word_freq[ww]


from heapq import nlargest
sel_len=int(len(sent_weight)*0.3)
summary=nlargest(sel_len,sent_weight,key=sent_weight.get)

summary_text=''.join(summary)
print(len(summary_text))