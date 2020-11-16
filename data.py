import random
from collections import namedtuple
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


class QAData():
    """
    Load the train/predecit/test data
    """

    def __init__(self):
        self.vocabulary = Vocabulary("P:/nj/wordEmbedding/vocab_all_1.txt")
        self.answers = pickle.load(open("./data/answers.pkl", 'rb'))
        dataset = pickle.load(open("P:/pkl/final.pkl", 'rb'))
        size_dataset = len(dataset)
        size_train = int(size_dataset * 0.8)
        size_test = int(size_dataset - size_train)
        print("Dataset Size = ",size_dataset,"\tTrain Size = ",size_train, "\tTest Size = ",size_test)
        self.training_set = dataset[:size_test]
        self.dec_timesteps = 150
        self.enc_timesteps = 150

    def pad(self, data, length):
        """
        pad the data to meet given length requirement

        Args:
            data (vector): vector of question or answer
            length(integer): length of desired vector
        """

        from keras.preprocessing.sequence import pad_sequences
        return pad_sequences(data, maxlen=length, padding='post', truncating='post', value=0)

    def get_training_data(self):
        """
        Return training question and answers
        """

        questions = []
        good_answers = []
        _answerPooling = []
        badanswer=[]
        for qa in self.training_set:
            _tmpPolling = qa['BadAnswers']
            if (_tmpPolling != None) and (len(_tmpPolling)>0):
                for _bad in _tmpPolling:
                    if len(_bad) > 2:
                        _answerPooling.append(_bad)
        random.shuffle(_answerPooling)
        for j, qa in enumerate(self.training_set):
            questions.extend([qa['QuestionText']] * len(qa['GoodAnswers']))
            good_answers.extend(qa['GoodAnswers'])
            diff = len(qa['GoodAnswers']) - len(qa['BadAnswers'])
            if diff >= 0:
                # داده هایی که لیبل بد دارند به لیست اضافه میشوند
                badanswer.extend(qa['BadAnswers'])
                
                # اگر دادهای بد کم بود
                # به همان مقدار رندوم از داده های پولینک جواب بردار
                # اگر داده های بد با خوب برابر بود عدد صفر است و اتفاقی نمیوفتد
                badanswer.extend(random.sample(_answerPooling, diff)) 
            if diff < 0:
                # اگر داده های بد بیشتر از داده های خوب بودند
                # به اندازه داده های خوب از داده های بد برمیداریم
                # و به لیست اضافه میکنیم و بقیه را دور میریزیم
                badanswer.extend(qa['BadAnswers'][:len(qa['GoodAnswers'])])

        # pad the question and answers
        questions = self.pad(questions, self.enc_timesteps)
        good_answers = self.pad(good_answers, self.dec_timesteps)
        bad_answers = self.pad(badanswer, self.dec_timesteps)

        return questions, good_answers, bad_answers

    def process_data(self, d):
        """
        Process the predection data
        """

        indices = d['good'] + d['bad']
        answers = self.pad([self.answers[i]
                            for i in indices], self.dec_timesteps)
        question = self.pad([d['question']] * len(indices), self.enc_timesteps)
        return indices, answers, question

    def process_test_data(self, question, answers):
        """
        Process the test data
        """

        answer_unpadded = []
        for answer in answers:
            print(answer.split(' '))
            answer_unpadded.append([self.vocabulary[word]
                                    for word in answer.split(' ')])
        answers = self.pad(answer_unpadded, self.dec_timesteps)
        question = self.pad([[self.vocabulary[word] for word in question.split(
            ' ')]] * len(answers), self.enc_timesteps)
        return answers, question
