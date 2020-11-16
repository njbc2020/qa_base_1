from PreParation import PreParation
import numpy as np
import pandas as pd
import random
import pickle
from gensim.models import Word2Vec
from collections import OrderedDict

_preparation = PreParation()    # لود کردن پیش پردازش
_Pooling = []       #   داده های جواب که به صورت موقت در این ظرف ریخته میشوند
Question = []       #   داده های سوال
GoodsAnswers = []   #   داده های جواب خوب
BadsAnswers = []    #   داده های جواب بد
Vocab = []
Vectors = []
wordNot = []

qa_Data = pd.read_json('data/NiniAll-1.json', encoding='utf8')
jsonData = qa_Data["qa"]

# این متد آبجکت (لیستی از جواب در فرمت پاندا) را ورودی میگیرد و پیش پردازش را روی آنها اعمال میکند
def cleanAnswer(answers):
    _answer = []
    for answer in answers:
        txt = answer["AnswerText"]
        if txt != None and txt != "" and txt != " ":
            _answer.append(txt)
    return _answer


for qa in jsonData:
    _bads = qa["BadAnswers"]
    _bads = cleanAnswer(_bads)
    _goods = qa["GoodAnswers"]
    _goods = cleanAnswer(_goods)
    _q = qa["QuestionText"]
    
    _Pooling.extend(_bads)
    _Pooling.extend(_goods)
    _Pooling.append(_q)

newSentence = []
sentences1 = []

for w in _Pooling:
    if w != None and w != '':
        try:
            txtClean = _preparation.cleanText(w)
            txtClean = _preparation.cleanText2(txtClean)
            sents = _preparation.token(txtClean)
            if sents != None and len(sents) > 0:
                for _sent in sents:
                    if _sent != '':
                        sentences1.append(_sent)
        except:
            newSentence.append(w)
            print("  Word: ",w)

print("________")

for text in sentences1:
    #_text = _preparation.cleanText2(text)
    Vocab.extend(_preparation.wordToken(text, removeExtra=True, stopword=True))

Vocab1 = list(OrderedDict.fromkeys(Vocab))
with open('data/vocab_Json_DataSet.pkl','wb')as f:
    pickle.dump(Vocab1, f)
    
new_model = Word2Vec.load('P:/pkl/newSentence.bin')

Vocab10=[]
Vectors.append(new_model.wv["نغمه"])
for word in Vocab1:
    if word.strip() in new_model.wv.vocab:
        Vectors.append(new_model.wv[word.strip()])
        Vocab10.append(word.strip())
    else:
        _w = _preparation.cleanText(word.replace("\u200c"," "))
        _w = _preparation.cleanText2(_w)
        words = _preparation.wordToken(_w)
        for _word in words:
            if (_word in new_model.wv.vocab) and (_word not in Vocab10):
                Vocab10.append(_word.strip())
                Vectors.append(new_model.wv[_word.strip()])
            else:
                wordNot.append(word)
#c = new_model.wv.most_similar("")
print("word Not Exists: ",len(wordNot))

vocab_all =[]
Vocab10.sort()
i=0
for _v in Vocab10:
    vocab_all.append( str(i+1) + " "+ _v)
    i+=1

embeddingsNp= np.array(Vectors)
with open('P:/nj/wordEmbedding/wordEmbedding_1.embedding', 'wb') as f:
    np.save(f, embeddingsNp)


f1 = open('P:/nj/wordEmbedding/vocab_1.txt', 'w', encoding='utf-8')
s1 = '\n'.join(Vocab10)
f1.write(s1)
f1.close()

f2 = open('P:/nj/wordEmbedding/vocab_all_1.txt', 'w', encoding='utf-8')
s1 = '\n'.join(vocab_all)
f2.write(s1)
f2.close()