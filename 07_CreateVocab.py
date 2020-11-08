f = open("vocab1.txt", "r", encoding='utf-8-sig')
_vocab = f.readlines()

vocab = []
i = 1
for v in _vocab:
    vocab.append(str(i)+" "+v)
    i += 1

f = open('vocab_all.txt', 'w', encoding='utf-8')
s1 = ''.join(vocab)
f.write(s1)
f.close()
