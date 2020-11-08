from PreParation import PreParation
import pandas as pd

_preparation = PreParation()
data = []
sentences = []
k = 1
vocab = []
Goods=[]

qa_Data = pd.read_json('data/NiniAll-1.json', encoding='utf8')
qqaa= qa_Data["qa"]
a = []
for qa in qqaa:
    _q = qa["QuestionText"]
    _goods = qa["GoodAnswers"]
    for good in _goods:
        Goods.append(good["AnswerText"])
    
q = list(qa_Data["QuestionText"])
_GoodAnswers = list(qa_Data["GoodAnswers"])
for answers in _GoodAnswers:
    # _answerText = answers["AnswerText"].astype(str).values.tolist()
    for answerText in answers:
        _a = answerText["AnswerText"]
        _a = _preparation.cleanText(_a)
        _a = _preparation.cleanText2(_a, True)
        a.append(_a)
for _q in q:
    if _q != None and _q != '':
        data.append(_q)
for _a in a:
    if _a != None and _a != '':
        data.append(_a)
        
vocab = []
for w in data:
    if k % 1000 == 0:
        print(k)
    k += 1
    if w != None and w != '':
        txtClean = _preparation.cleanText(w)
        sents = _preparation.token(txtClean)
        if sents != None and len(sents) > 0:
            for _sent in sents:
                txt = _preparation.cleanText2(_sent)
                if txt != '':
                    sentences.append(txt)
        txt = _preparation.cleanText2(txtClean)
        for _tk in txt.split():
            vocab.append(_tk)

vocab = list(dict.fromkeys(vocab)).sort()

f = open('data/vocab_all_.txt', 'w', encoding='utf-8')
s1 = '\n'.join(vocab)
f.write(s1)
f.close()

f = open('data/sentences_.txt', 'w', encoding='utf-8')
s2 = '\n'.join(sentences)
f.write(s2)
f.close()
