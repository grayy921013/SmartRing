import numpy
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing import sequence
from sklearn.utils import shuffle

X = []
Y = []
for i in range(0, 10):
    files = os.listdir(str(i))
    for file in files:
        X.append(numpy.loadtxt(open(str(i) + "/" + file, "rb"), delimiter=","))
        y = numpy.zeros(10)
        y[i] = 1
        Y.append(y)
X = numpy.asarray(X)
Y = numpy.asarray(Y)
max_review_length = 200
X = sequence.pad_sequences(X, maxlen=max_review_length)
X, Y = shuffle(X, Y, random_state=0)
total_size = X.shape[0]
train_size = int(total_size * 0.8)
X_train = X[:train_size, :, :]
Y_train = Y[:train_size]
X_test = X[train_size:, :, :]
Y_test = Y[train_size:]
model = Sequential()
model.add(LSTM(output_dim=4, input_shape=(max_review_length, 6), return_sequences=True))
model.add(LSTM(100))
model.add(Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, Y_train, nb_epoch=200, batch_size=64)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))