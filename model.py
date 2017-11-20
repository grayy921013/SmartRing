from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Activation, LSTM, Merge, TimeDistributedDense
from keras.optimizers import SGD
import config

#
# this script is for defining different models for testing
#

def fork (model, n=2):
    forks = []
    for _ in range(n):
        f = Sequential()
        f.add(model)
        forks.append(f)
    return forks

def get_model(hps = None, TAG = None, bidirection=False):
    if TAG is None:
        print ('use default model')
    if hps is None:
        return default_model()
    if bidirection:
        return bidirectional_model(hps)
    return default_model(hps)

def default_model(hps):
    model = Sequential()
    model.add(LSTM(output_dim=hps[0], input_shape=(config.max_review_length, 6), return_sequences=True))
    model.add(Dropout(hps[1]))
    model.add(LSTM(hps[2]))
    model.add(Dropout(hps[3]))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def bidirectional_model(hps):
    forward = Sequential()
    forward.add(LSTM(output_dim=hps[0], input_shape=(config.max_review_length, 6), return_sequences=True))
    backward = Sequential()
    backward.add(LSTM(output_dim=hps[0], input_shape=(config.max_review_length, 6),
                      return_sequences=True, go_backwards=True))
    model = Sequential()
    model.add(Merge([forward, backward], mode='concat'))
    model.add(Dropout(hps[1]))

    forward_2, backward_2 = fork(model)

    forward_2.add(LSTM(hps[2]))
    backward_2.add(LSTM(hps[2], go_backwards=True))

    model = Sequential()
    model.add(Merge([forward_2, backward_2], mode='concat'))
    model.add(Dropout(hps[3]))

    model.add(TimeDistributedDense(output_dim=10))
    model.add(Activation('softmax'))
    sgd = SGD(lr=0.1, decay=1e-5, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
