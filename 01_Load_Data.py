import pickle
import pandas as pd
import numpy as np
import random

class Vocabulary(dict):
    """
    Bi-directional look up dictionary for the vocabulary

    Args:
        (dict): the default python dict class is extended
    """

    def __init__(self, vocabulary_file_name):
        with open(vocabulary_file_name , encoding="utf-8") as vocabulary_file:
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

def writeCsv(data1):
    nppp = np.array(data1)
    df = pd.DataFrame(data=nppp)
    df.to_csv("Csv_Token_" + str(random.randint(1,9999))+".csv.txt")
    print("Export CSV File Success!\n")

vocabulary = Vocabulary("vocab_all.txt")
aaaaaa = vocabulary["خانه"]
answers = pickle.load(open("./data/answers.pkl", 'rb'))
train = pickle.load(open("./data/train.pkl", 'rb'))
questions = []
good_answers = []
aa = enumerate(train)
for j, qa in enumerate(train):
    aa = [qa['question']]
    bb = len(qa['answers'])
    cc = [qa['question']] * len(qa['answers'])
    questions.extend([qa['question']] * len(qa['answers']))
    good_answers.extend([answers[i] for i in qa['answers']])

dev = pickle.load(open("./data/dev1.pkl", 'rb'))
print (answers[5])
ans= answers.values()
d12=[]
for a in ans:
    d12.append(a)

print(len(d12))

writeCsv(d12)