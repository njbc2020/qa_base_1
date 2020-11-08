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
        with open(vocabulary_file_name) as vocabulary_file:
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


vocabulary = Vocabulary("./data/vocab_all.txt")
dec_timesteps = 150
enc_timesteps = 150
answers = pickle.load(open("./data/answers.pkl", 'rb'))
# writeCsv(answers)
ans= answers.values()
d12=[]
for a in ans:
    d12.append(a)

print(len(d12))
npp= np.array(ans)
# f = open("demofile3.txt",'w')
# f.writelines(npp)
# f.close()
##df = pd.DataFrame(data=d12)
writeCsv(d12)
training_set = pickle.load(open("./data/train.pkl", 'rb'))

answer1 = ""
for a in answers[1]:
    answer1 = answer1 + vocabulary[a] + " "

print(answer1)


with open('./data/answers.pkl', 'rb') as f:
    data = pickle.load(f)

with open('./data/train.pkl', 'rb') as f1:
    data1 = pickle.load(f1)
print("___________", "\n")
# print(data1[1])
# print(data1[500])
# print(data1[1020])
# print(data1[5001])
print("___________")
g = 1
