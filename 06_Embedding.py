from keras.layers import Input, Embedding, Subtract, Lambda
import keras.backend as K
from keras.models import Model

f = open("sentences.txt", "r", encoding='utf-8-sig')
_sentences = f.readlines()

embed_dim = 300

model = Sequential()
model.add(Embedding(max_fatures, embed_dim,input_length = X.shape[1]))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print(model.summary())
# fit the model
model.fit(padded_docs, labels, epochs=50, verbose=0)

