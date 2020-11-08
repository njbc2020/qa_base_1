#region Init
#%% Import and init
import json
import pandas as pd
import numpy as np
from hazm import Normalizer, word_tokenize, sent_tokenize, Lemmatizer
from hazm import WordTokenizer
import time
from gensim.models import Word2Vec
import pickle
import os.path
normalizer = Normalizer()
#endregion

#region Load
# LoadFile 
sw = pd.read_csv("data/stop_words/stpwrd.csv")
sw = sw["StopWord"].astype(str).values.tolist()
sw.append("باسلام")
sw.append("سلام")
sw.append("(")
sw.append(")")
#endregion

#region Functions
#%% Functions
def flatten(A):
    rt = []
    for i in A:
        if isinstance(i, list):
            rt.extend(flatten(i))
        else:
            rt.append(i.strip())
    return rt

def cleanTxt(txt):
    txt = txt.replace("ً","").replace("ٍ","").replace("ً","").replace("؛"," ").replace(","," ").replace("َ","").replace("ُ","").replace("ِ","").replace("ّ","").replace("إ","ا").replace("أ","ا")
    return txt

def clean_persianText(txt):
    #txt = str(txt)
    
    txt = cleanTxt(txt)
    txt = normalizer.character_refinement(txt)
    txt = normalizer.affix_spacing(txt)
    txt = normalizer.punctuation_spacing(txt)
    txt = normalizer.normalize(txt)
    
    return txt

def prepare_data(data):
    s = time.time()
    ##data = np.array(data)
    data1 = []
    data1.clear
    for x in data:
        data1.append(clean_persianText(x))
    
    e = time.time()
    print("prepare_data Time: ",e - s," !")
    print("Prepare Done\nStart Flatten\n")
    return flatten(data1)

def stop_word(data):
    
    # with open("data/stop_words/stopwords.txt") as f:
    #     content = f.readlines()
    #     [sw.append(x.strip()) for x in content]
    #     sw=set(sw)
    new_data=[]
    for text in data:
        text = text.replace("\n"," ")
        text = text.replace("..","")
        text = text.replace(".","").strip()
        text = (' '.join([word for word in text.split() if word not in sw])).replace("  "," ")
        if text != " " and text != "" and text != "." and text != "  " and text != ".":
            new_data.append(' '.join([word for word in text.split() if word not in sw]).lower())
    return new_data

def tok(dataTok):
    normalizer = Normalizer()
    tokenizer = WordTokenizer(join_verb_parts=False, replace_links=True, replace_IDs=True, replace_numbers=True, replace_hashtags=True)
    s = time.time()
    ij = 0
    #dataTok.apply (lambda x: dataTok1.append(sent_tokenize(x)) )
    
    for row in dataTok:
        _sents = sent_tokenize(row)
        _sents= stop_word(_sents)
        for _sent in _sents:
            _temp = _sent.replace(".","").replace(",","").replace("،","").replace("؛","").strip()
            _wrds = []
            _wrds = normalizer.normalize(_temp)
            dataTok1.append(tokenizer.tokenize(_wrds))
    
   
    print("Data: ", dataTok1.__len__())
    e = time.time()
    print("Tokenize Done, Time: ",e - s," !\n")

def writeJson(data):
    dataTemplate = {'ReviewsTokenize': data}
    df = pd.DataFrame(data=dataTemplate)
    with open("token.json", "w", encoding='utf-8') as jsonfile:
        json.dump(dataTemplate, jsonfile, ensure_ascii=False)
    print("\nExport JSON File Success!\n")

def writeCsv(data):
    from datetime import datetime
    df = pd.DataFrame(data=data)
    df.to_csv("Csv_Token_"+ str(datetime.now())+".csv.txt")
    print("Export CSV File Success!\n")

print("function pass")
#endregion

#region DataLoad
# with open("cqa/answer_clean.txt", "r",encoding="utf8") as f:
#     a_raw = f.readlines()
# with open("cqa/Question_Body_clean.txt", "r",encoding="utf8") as f:
#     q_raw = f.readlines()
f = open("data/sentences.txt", "r", encoding="utf8")
sentence = f.readlines()
newSentence = []

# for qq in q_raw:
#     a_raw.append(qq)

dataTok1=[]
data=[]
data = sentence
print(len(data))

# %%
if os.path.isfile('data2.pkl'):
    data2 = pickle.load( open( "data2.pkl", "rb" ) )
else:
    data2 = prepare_data(data)
    with open('data2.pkl','wb')as f:
        pickle.dump(data2, f)

# %%
if os.path.isfile('dataTok1.pkl'):
    dataTok1 = pickle.load( open( "dataTok1.pkl", "rb" ) )
else:
    tok(data2)
    with open('dataTok1.pkl','wb')as f:
        pickle.dump(dataTok1, f)
data2=""
#writeJson(dataTok1)
#writeCsv(dataTok1)

# %%
print("#######\n______________\n\n1111111111111111\n\n\n\n Start Word To Vector: \n\n")

model = Word2Vec(dataTok1, min_count=1,)
# summarize the loaded model
print(model)
# summarize vocabulary
#words = list(model.wv.vocab)
model.save('model_qa.bin')
# load model
#new_model = Word2Vec.load('model2.bin')
#print(new_model)