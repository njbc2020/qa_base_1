from PreParation import PreParation

_preparation = PreParation()
data = []
sentences = []
k = 1
vocab = []


f = open("Question_Body.txt", "r", encoding='utf-8-sig')
q = f.readlines()
f = open("answer_clean.txt", "r", encoding='utf-8-sig')
a = f.readlines()
for _q in q:
    data.append(_q)
for _a in a:
    data.append(_a)

for w in data:
    if k % 1000 == 0:
        print(k)
    k += 1
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


f = open('vocab.txt', 'w', encoding='utf-8')
s1 = '\n'.join(vocab)
f.write(s1)
f.close()

f = open('sentences.txt', 'w', encoding='utf-8')
s2 = '\n'.join(sentences)
f.write(s2)
f.close()
