import numpy
import os
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
numpy.save('X_train', X_train)
numpy.save('X_test', X_test)
numpy.save('Y_train', Y_train)
numpy.save('Y_test', Y_test)