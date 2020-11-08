#from parsivar import Normalizer, FindStems
from parsivar import FindStems, Normalizer
# from hazm import word_tokenize
import hazm.Normalizer as HazmNormal
import re
import pandas as pd
from parsivar import Tokenizer
my_tokenizer = Tokenizer()

k = 1
data = []
sentences = []

sw = pd.read_csv("data/stop_words/stpwrd.csv")
sw = sw["StopWord"].astype(str).values.tolist()
sw.append("باسلام")
sw.append("سلام")
sw.append("(")
sw.append(")")

my_normalizer = Normalizer(
    statistical_space_correction=True, date_normalizing_needed=True)
normalizer = Normalizer()
my_stemmer = FindStems()


def stop_word(data):
    text = data.replace("..", " ")
    text = text.replace(".", " ")
    text = text.replace("  ", " ").replace("  ", " ")
    text = (' '.join([word for word in data.split()
                      if word not in sw])).replace("  ", " ")
    if text != " " and text != "" and text != "." and text != "  " and text != ".":
        return ' '.join([word for word in text.split() if word not in sw])
    else:
        return ''


persianmix = re.compile(
    "(([\u0600-\u06FF]+)([0-9]+)|([0-9]+)([\u0600-\u06FF]+)|([a-zA-Z]+)([0-9]+)|([0-9]+)([a-zA-Z]+))")
num = re.compile('\d')


def splitnumber(txt):
    if num.search(txt) != None:
        res = persianmix.match(txt).groups()
        return (" ".join([word for word in res[1:] if word != None]))
    return txt


def Stem(txt):
    _txt = my_stemmer.convert_to_stem(txt).split('&')
    return _txt[0]


def removeIrritate(txt):
    return re.compile(r'(.)\1{2,}', re.IGNORECASE).sub(r'\1', txt)


def cleanText(txt):
    txt = w.replace("\u200c", " ")
    txt = txt.replace("آ", "ا")
    #txt = stop_word(txt)
    txt = removeIrritate(txt)
    txt = my_normalizer.normalize(txt)
    txt = txt.replace('"', ' ').replace("+", " ").replace("{", " ").replace("}", " ").replace("-", " ").replace("(", " ").replace(")", " ").replace("_", " ").replace("$", " ").replace("#", " ").replace("'", " ").replace("/", " ").replace(
        "\\", " ").replace("*", " ").replace("@", " ").replace("ً", "").replace("ٍ", "").replace("ً", "").replace("َ", "").replace("ُ", "").replace("ِ", "").replace("ّ", "").replace("إ", "ا").replace("أ", "ا").replace("÷", " ").replace("=", " ").replace("[", " ").replace("]", " ").replace("»", " ").replace("~", " ").replace("٪", " ").replace("ْ", "").replace("¿", " ")
    txt = txt.replace("    ", " ").replace(
        "   ", " ").replace("  ", " ").replace("  ", " ")
    txt = txt.replace("\u200c", " ")
    txt1 = []
    for t in txt.split():
        try:
            t = splitnumber(t)
        except:
            pass
        for _t in t.split():
            w1 = Stem(_t)
            txt1.append(w1)
    #txt = stop_word(txt)
    #tks = txt.split()
    return ' '.join(txt1)

def cleanText2(txt):
    _txt = stop_word(txt)
    _txt = _txt.replace('.', ' ').replace("?", " ").replace("؛", " ").replace(",", " ").replace("؟", " ").replace(";", " ").replace("!", " ").replace(":", " ").replace("    ", " ").replace(
        "   ", " ").replace("  ", " ").replace("  ", " ")
    _txt = stop_word(_txt)
    return _txt

def token(txt):
    sents = my_tokenizer.tokenize_sentences(txt)
    if sents != None and len(sents)>0:
        for _sent in sents:
            txt = cleanText2(_sent)
            if txt != '':
                sentences.append(txt)



f = open("Question_Body.txt", "r", encoding='utf-8-sig')
q = f.readlines()
f = open("answer_clean.txt", "r", encoding='utf-8-sig')
a = f.readlines()
for _q in q:
    data.append(_q)
for _a in a:
    data.append(_a)
vocab = []
for w in data:
    if k % 1000 == 0:
        print(k)
    k += 1
    txtClean = cleanText(w)
    token(txtClean)
    txt = cleanText2(txtClean)
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
