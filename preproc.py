import os
import numpy
from keras.preprocessing import sequence
from sklearn.utils import shuffle
import config

def get_raw_input():
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
    return X,Y


def get_train_test():
    X,Y = get_raw_input()

    X = sequence.pad_sequences(X, maxlen=config.max_review_length)
    X, Y = shuffle(X, Y, random_state=0)
    total_size = X.shape[0]
    train_size = int(total_size * 0.8)
    X_train = X[:train_size, :, :]
    Y_train = Y[:train_size]
    X_test = X[train_size:, :, :]
    Y_test = Y[train_size:]
    return X_train, Y_train, X_test, Y_test