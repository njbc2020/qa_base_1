from PreParation import PreParation
import pandas as pd
import random
import pickle

class Vocabulary(dict):
    """
    Bi-directional look up dictionary for the vocabulary

    Args:
        (dict): the default python dict class is extended
    """

    def __init__(self, vocabulary_file_name):
        with open(vocabulary_file_name, encoding="utf8") as vocabulary_file:
            for line in vocabulary_file:
                key, value = line.split()
                self[int(key)] = value
        self[0] = '<PAD>'

    def __setitem__(self, key, value):
        if key in self:
            raise Exception('Repeat Key', key)
        if value in self:
            raise Exception('Repeat value', value)
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        return dict.__len__(self) // 2

vocabulary = Vocabulary("P:/nj/wordEmbedding/vocab_all.txt")

_preparation = PreParation()    # لود کردن پیش پردازش
_answerPooling = [] #   داده های جواب که به صورت موقت در این ظرف ریخته میشوند
Question = []       #   داده های سوال
GoodsAnswers = []   #   داده های جواب خوب
BadsAnswers = []    #   داده های جواب بد

qa_Data = pd.read_json('data/NiniAll-1.json', encoding='utf8')
vocab=[]
for v in vocabulary.values():
    vocab.append(v)
qqaa = qa_Data["qa"]

def cleanText(txt):
    txt = _preparation.cleanText(txt)
    txt = _preparation.cleanText2(txt)
    return txt

# این متد آبجکت (لیستی از جواب در فرمت پاندا) را ورودی میگیرد و پیش پردازش را روی آنها اعمال میکند
def cleanAnswer(answers):
    _answer = []
    for answer in answers:
        txt = answer["AnswerText"]
        txt = cleanText(txt)
        sents = _preparation.token(txt)
        ans = []
        ans1= []
        if sents != None and len(sents) > 0:
            for _sent in sents:
                if _sent != '':
                    words =_preparation.wordToken(_sent, removeExtra=True, stopword=True)
                    for word in words:
                        if word in vocab:
                            vocabulary
                        else:
                            _w = _preparation.cleanText(word.replace("\u200c"," "))
                            _w = _preparation.cleanText2(_w)
                            _words = _preparation.wordToken(_w)
                            for _word in _words:
                                if _word in vocab:
                                    ans.append(_word)
                                    ans1.append(vocabulary[_word])
                                else:
                                    print("       \t Error \t     ...")
                    
    return _answer


for qa in qqaa:
    _bads = qa["BadAnswers"]
    _bads = cleanAnswer(_bads)
    _answerPooling.extend(_bads)

print("________")

for qa in qqaa:
    _q = qa["QuestionText"]
    q = _preparation.cleanText(_q)
    q = _preparation.cleanText2(q, stopword=True)

    _goods = qa["GoodAnswers"]
    _bads = qa["BadAnswers"]

    goods = cleanAnswer(_goods)
    bads = cleanAnswer(_bads)
    diff = len(goods) - len(bads)
    # به تعداد داده های خوب سوال را در لیست ااضافه میکنیم
    Question.extend(q * len(goods))
    GoodsAnswers.extend(goods)
    if diff >= 0:
        # داده هایی که لیبل بد دارند به لیست اضافه میشوند
        BadsAnswers.extend(bads)
        
        # اگر دادهای بد کم بود
        # به همان مقدار رندوم از داده های پولینک جواب بردار
        # اگر داده های بد با خوب برابر بود عدد صفر است و اتفاقی نمیوفتد
        BadsAnswers.extend(random.sample(_answerPooling, diff)) 
    if diff < 0:
        # اگر داده های بد بیشتر از داده های خوب بودند
        # به اندازه داده های خوب از داده های بد برمیداریم
        # و به لیست اضافه میکنیم و بقیه را دور میریزیم
        BadsAnswers.extend(bads[:len(goods)])

# در نهایت داده های بدست آمده را در فایل باینری ذخیره میکنیم
with open('data/Question.pkl','wb')as f:
    pickle.dump(Question, f)

with open('data/GoodsAnswers.pkl','wb')as f:
    pickle.dump(GoodsAnswers, f)

with open('data/BadsAnswers.pkl','wb')as f:
    pickle.dump(BadsAnswers, f)