# %%
#from parsivar import Normalizer, FindStems
from parsivar import FindStems
from hazm import Normalizer, word_tokenize
import re

tmp_text = "به گزارش ایسنا سمینار شیمی آلی از امروز ۱۱ شهریور ۱۳۹۶ در دانشگاه علم و صنعت ایران آغاز به کار کرد. این سمینار تا ۱۳ شهریور ادامه می یابد."
# my_normalizer = Normalizer(
#     statistical_space_correction=True, date_normalizing_needed=True)
normalizer = Normalizer()
#my_tokenizer = Tokenizer()
my_stemmer = FindStems()
# print(my_normalizer.normalize(tmp_text))
# print(my_stemmer.convert_to_stem("آمدم").split('&')[1])


def Stem(txt):
    _txt = my_stemmer.convert_to_stem(txt).split('&')
    return _txt[0]


def removeIrritate(txt):
    return re.compile(r'(.)\1{2,}', re.IGNORECASE).sub(r'\1', txt)

# %%

# txt = txt.replace("\u200c", " ")
# txt1 = my_normalizer.normalize(txt)


data = []

# f = open("Question_Body.txt", "r", encoding='utf-8-sig')
# q = f.readlines()
# f = open("answer_clean.txt", "r", encoding='utf-8-sig')
# a = f.readlines()
# for _q in q:
data.append("سلام سلام خوبی سلام")

vocab = []

for w in data:
    txt = w.replace("\u200c", " ")
    txt = removeIrritate(txt)
    txt = normalizer.character_refinement(txt)
    txt = normalizer.affix_spacing(txt)
    txt = normalizer.punctuation_spacing(txt)
    txt = txt.replace('.', '')
    txt = normalizer.normalize(txt)

    #txt = my_normalizer.normalize(txt)
    tks = txt.split()
    for tk in tks:
        w = Stem(tk)
        r1 = w in vocab
        r2 = not(w in vocab)
        if not w in vocab:
            vocab.append(w)
f = open('vocab.txt', 'w', encoding='utf-8')
s1 = '\n'.join(vocab1)
f.write(s1)
f.close()
h = "ttttttttttttttttt"

# %%
