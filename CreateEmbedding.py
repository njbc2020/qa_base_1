from PreParation import PreParation
import pandas as pd
import numpy as np
import random
import time
import pickle
from gensim.models import Word2Vec

_preparation = PreParation()    # لود کردن پیش پردازش
data = []
sentences1 = []
k = 1
vocab = []

#region Part1 - Beytoote Load
# bey=[]
# beytoote = pd.read_json('data/b_p1.json', encoding='utf8')["data"]
# for _article in beytoote:
#     bey.append(_article["Title"])
#     if _article["Paragraphs"] != None:
#         bey.extend(_article["Paragraphs"])
# beytoote = pd.read_json('data/b_p2.json', encoding='utf8')["data"]
# for _article in beytoote:
#     bey.append(_article["Title"])
#     if _article["Paragraphs"] != None:
#         bey.extend(_article["Paragraphs"])
# ff = open('data/Beytoote.txt', 'w', encoding='utf-8')
# s1 = '\n'.join(bey)
# ff.write(s1)
# ff.close()
#endregion

#region Part2
# def Answer(answers):
#     _answer = []
#     for answer in answers:
#         txt = answer["AnswerText"]
#         if txt != None and txt != "" and txt != " ":
#             _answer.append(txt)
#     return _answer

# qa_Data = pd.read_json('data/NiniAll-1.json', encoding='utf8')
# jsonData = qa_Data["qa"]
# f = open("data/Beytoote1.txt", "r", encoding="utf8")
# bey = f.readlines()
# f = open("data/sentences.txt", "r", encoding="utf8")
# sentence = f.readlines()
# f = open("Question_Body.txt", "r", encoding='utf-8-sig')
# q = f.readlines()
# f = open("answer_clean.txt", "r", encoding='utf-8-sig')
# a = f.readlines()
# sentence.extend(bey)
# sentence.extend(q)
# sentence.extend(a)
# for qa in jsonData:
#     _bads = qa["BadAnswers"]
#     _bads = Answer(_bads)
#     _goods = qa["GoodAnswers"]
#     _goods = Answer(_goods)
#     _q = qa["QuestionText"]
    
#     sentence.extend(_bads)
#     sentence.extend(_goods)
#     sentence.append(_q)

# print("--- Load All Data : ",len(sentence)," ---")
# newSentence = []

# vocab = []
# s = time.time()
# for w in sentence:
#     if k % 1000 == 0:
#         e = time.time()
#         print(k," \t Time: ",e-s,"s")
#         s = time.time()
#     k += 1
#     if w != None and w != '':
#         try:
#             txtClean = _preparation.cleanText(w)
#             txtClean = _preparation.cleanText2(txtClean)
#             sents = _preparation.token(txtClean)
#             if sents != None and len(sents) > 0:
#                 for _sent in sents:
#                     if _sent != '':
#                         sentences1.append(_sent)
#             # txt = _preparation.cleanText2(txtClean)
#             # for _tk in txt.split():
#             #     vocab.append(_tk)
#         except:
#             newSentence.append(w)
#             print("k: ",k,"  Word: ",w)


# with open('data/sentence_all_bey.pkl','wb')as f:
#     pickle.dump(sentences1, f)
# with open('data/sentence_newSentence.pkl','wb')as ff:
#     pickle.dump(newSentence, ff)

#endregion

#region Part3 - Word Tokenize For Word Embedding
# sentences1 = pickle.load(open("data/sentence_all_bey.pkl", "rb"))
# newSentence = []
# a = 0
# for sen in sentences1:
#     newSentence.append(_preparation.wordToken(sen, removeExtra=True, stopword=True))
#     a += 1
#     if a % 10000 == 0:
#         print("\r Count: \t  ", a, "  ")
#     # if a > 10000:
#     #     break
# with open('P:/pkl/newSentence_split.pkl', 'wb')as ff:
#     pickle.dump(newSentence, ff)
#endregion

#region Part4
# newSentence = pickle.load(open("P:/pkl/newSentence_split.pkl", "rb"))
# print("-----\t Sentence Load , count= ",len(newSentence)," \t-----")
# model = Word2Vec(newSentence, size=100, window=5, min_count=1, workers=4)
# print(model)
# model.save('P:/pkl/newSentence.bin')
#endregion

# load model
new_model = Word2Vec.load('P:/pkl/newSentence.bin')
a = new_model.wv.most_similar("پوشک")
b = new_model.wv.most_similar("دود")
c = new_model.wv.most_similar("پاسداران")
d = new_model.wv.most_similar("باو")

z = 1
# wordsss = ['کلمه', 'سخت', 'کوفتتتتتهتبریزیی', 'عباااااس']
# wordNot = []
# vvectorss = []
# for word in wordsss:
#     if word in new_model.wv.vocab:
#         vvectorss.append(new_model.wv[word])
#     else:
#         wordNot.append(word)
# #c = new_model.wv.most_similar("")
# print(new_model)
