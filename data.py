import os
import numpy
from keras.preprocessing import sequence
from sklearn.utils import shuffle
import config
import random

def get_raw_input():
    X = []
    Y = []
    for i in range(0, 10):
        files = os.listdir(str(i))
        for file in files:
            try:
                X.append(numpy.loadtxt(open(str(i) + "/" + file, "rb"), delimiter=","))
                y = numpy.zeros(10)
                y[i] = 1
                Y.append(y)
            except:
                print(str(i) + file.title())
                print("data corruption")
    X = numpy.asarray(X)
    Y = numpy.asarray(Y)
    return X, Y

def get_new_input():
    X = []
    Y = []
    for i in range(0, 10):
        files = os.listdir(str(i))
        for file in files:
            try:
                if file > "2017-11-22":
                    X.append(numpy.loadtxt(open(str(i) + "/" + file, "rb"), delimiter=","))
                    y = numpy.zeros(10)
                    y[i] = 1
                    Y.append(y)
            except:
                print("data corruption")
    X = numpy.asarray(X)
    Y = numpy.asarray(Y)
    return X, Y

def get_calibrate_raw_input():
    X = []
    Y = []
    for i in ['DOWN', 'RIGHT']:
        files = os.listdir(str(i))
        for file in files:
            try:
                X.append(numpy.loadtxt(open(str(i) + "/" + file, "rb"), delimiter=","))
                y = numpy.zeros(2)
                if i == 'DOWN':
                    y[0] = 1
                else :
                    y[1] = 1
                Y.append(y)
            except:
                print("data corruption")
    X = numpy.asarray(X)
    Y = numpy.asarray(Y)
    return X, Y


def get_from_folder(dir):
    X = []
    Y = []
    for i in range(0, 10):
        files = os.listdir(dir + "/" + str(i))
        for file in files:
            try:
                X.append(numpy.loadtxt(open(dir + "/" + str(i) + "/" + file, "rb"), delimiter=","))
                y = numpy.zeros(10)
                y[i] = 1
                Y.append(y)
            except:
                print(str(i) + file.title())
                print("data corruption")
    X = numpy.asarray(sequence.pad_sequences(X, maxlen=config.max_review_length))
    Y = numpy.asarray(Y)
    return X, Y


def get_train_test():
    get_train_test(get_raw_input, config.max_review_length)

def get_train_test(get_data_method, maxlen):
    X, Y = get_data_method()
    X = sequence.pad_sequences(X, maxlen=maxlen)
    X, Y = shuffle(X, Y, random_state=999)
    total_size = X.shape[0]
    train_size = int(total_size * 0.8)
    X_train = X[:train_size, :, :]
    Y_train = Y[:train_size]
    X_test = X[train_size:, :, :]
    Y_test = Y[train_size:]
    return X_train, Y_train, X_test, Y_test

def get_train_test_npy():
    X_train = numpy.load('X_train.npy')
    X_test = numpy.load('X_test.npy')
    Y_train = numpy.load('Y_train.npy')
    Y_test = numpy.load('Y_test.npy')
    return X_train, Y_train, X_test, Y_test


def get_train_test_rounded_npy():
    X_train = numpy.load('X_train_rounded.npy')
    X_test = numpy.load('X_test_rounded.npy')
    Y_train = numpy.load('Y_train.npy')
    Y_test = numpy.load('Y_test.npy')
    print('use rounded data as input')
    return X_train, Y_train, X_test, Y_test


def get_train_test_scale_npy():
    X_train = numpy.load('X_train.max-min-abs-scale.npy')
    X_test = numpy.load('X_test.max-min-abs-scale.npy')
    Y_train = numpy.load('Y_train.npy')
    Y_test = numpy.load('Y_test.npy')
    print('use scale data as input')
    return X_train, Y_train, X_test, Y_test


def add_noise(X, Y):
    y = numpy.repeat(Y, 10, axis=0)
    size = len(X)
    times = 10
    max_len = config.max_review_length
    noise = [numpy.random.normal(0, 60, 6 * max_len).astype(int).reshape(max_len, 6) for i in range(size * times)]
    noises = numpy.array(noise)
    x = []
    for i in range(len(X)):
        for j in range(times):
            x.append(X[i] + noises[i * times + j])
    x = numpy.array(x)
    return x.astype(int), y.astype(float)


def get_data(data):
    if data == "round":
        return get_train_test_rounded_npy()
    elif data == "scale":
        return get_train_test_scale_npy()
    else:
        return get_train_test_npy()


def generate_full():
    X, Y = get_raw_input()
    X = sequence.pad_sequences(X, maxlen=config.max_review_length)
    X, Y = shuffle(X, Y, random_state=0)
    total_size = X.shape[0]
    train_size = int(total_size * 0.8)
    val_size = int(total_size * 0.9)
    X_train = X[:train_size, :, :]
    Y_train = Y[:train_size]
    X_val = X[train_size:val_size, :, :]
    Y_val = Y[train_size:val_size]
    X_test = X[val_size:, :, :]
    Y_test= Y[val_size:]
    print(X_train.shape[0], X_val.shape[0], X_test.shape[0])
    numpy.save("X_train_full", X_train)
    numpy.save("Y_train_full", Y_train)
    numpy.save("X_val_full", X_val)
    numpy.save("Y_val_full", Y_val)
    numpy.save("X_test_full", X_test)
    numpy.save("Y_test_full", Y_test)


def generate_full_with_noise():
    X, Y = get_raw_input()
    X, Y = shuffle(X, Y, random_state=0)
    total_size = X.shape[0]
    train_size = int(total_size * 0.8)
    val_size = int(total_size * 0.9)
    X_train = X[:train_size]
    Y_train = Y[:train_size]
    X_val = X[train_size:val_size]
    Y_val = Y[train_size:val_size]
    X_test = X[val_size:]
    Y_test= Y[val_size:]

    # Add gaussian noise and random repeat
    X = []
    Y = []
    times = 10
    for i in range(X_train.shape[0]):
        x = X_train[i]
        y = Y_train[i]
        X.append(x)
        Y.append(y)
        for i in range(times):
            new_x = []
            index = 0
            while index < x.shape[0]:
                noise = numpy.random.normal(0, 200, 3).astype(int)
                noise = numpy.append(noise, numpy.random.normal(0, 30, 3).astype(int))
                new_x.append(x[index] + noise)
                if random.random() > 0.2:
                    # 20% possibility to repeat current data point
                    index += 1
            new_x = numpy.asarray(new_x, int)
            X.append(new_x)
            Y.append(y)


    X = numpy.asarray(X)
    Y = numpy.asarray(Y)
    X = sequence.pad_sequences(X, maxlen=config.max_review_length)
    print(X.shape)
    X_val = sequence.pad_sequences(X_val, maxlen=config.max_review_length)
    X_test = sequence.pad_sequences(X_test, maxlen=config.max_review_length)

    numpy.save("X_train_full_noise", X)
    numpy.save("Y_train_full_noise", Y)
    numpy.save("X_val_full_noise", X_val)
    numpy.save("Y_val_full_noise", Y_val)
    numpy.save("X_test_full_noise", X_test)
    numpy.save("Y_test_full_noise", Y_test)



def get_full_data_npy():
    X_train = numpy.load('X_train_full.npy')
    X_val = numpy.load('X_val_full.npy')
    X_test = numpy.load('X_test_full.npy')
    Y_train = numpy.load('Y_train_full.npy')
    Y_val = numpy.load('Y_val_full.npy')
    Y_test = numpy.load('Y_test_full.npy')
    print('use full data as input')
    return X_train, Y_train, X_val, Y_val, X_test, Y_test


def get_full_data_with_noise_npy():
    X_train = numpy.load('X_train_full_noise.npy')
    X_val = numpy.load('X_val_full_noise.npy')
    X_test = numpy.load('X_test_full_noise.npy')
    Y_train = numpy.load('Y_train_full_noise.npy')
    Y_val = numpy.load('Y_val_full_noise.npy')
    Y_test = numpy.load('Y_test_full_noise.npy')
    print('use full data with noise as input')
    return X_train, Y_train, X_val, Y_val, X_test, Y_test

def get_calibrate_data_npy():
    X_train = numpy.load('./calibrate/X_train.npy')
    X_test = numpy.load('./calibrate/X_test.npy')
    Y_train = numpy.load('./calibrate/Y_train.npy')
    Y_test = numpy.load('./calibrate/Y_test.npy')
    print('use full data with noise as input')
    return X_train, Y_train, X_test, Y_test

