from parsivar import Tokenizer
my_tokenizer = Tokenizer()

f = open("Sentence.txt", "r", encoding='utf-8-sig')
_sentences = f.readlines()

sentences = []

for _sentence in _sentences:
    sents = my_tokenizer.tokenize_sentences(_sentence)
