from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Activation, LSTM, Merge, TimeDistributed, Bidirectional
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

def get_model(hps = None, TAG = None, bidirection=False, multiple=False):
    if TAG is None:
        print ('use default model')
    if TAG is 'best':
        return best_model()
    if hps is None:
        return default_model()
    if multiple:
        return multiple_rnn(hps)
    if bidirection:
        return bidirectional_model(hps)
    return default_model(hps)

def default_model():
    model = Sequential()
    model.add(LSTM(output_dim=4, input_shape=(config.max_review_length, 6), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(100))
    model.add(Dropout(0.2))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def best_model():
    model = Sequential()
    model.add(LSTM(output_dim=4, input_shape=(config.max_review_length, 6), return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(100))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def bidirectional_model(hps):
    model = Sequential()
    model.add(Bidirectional(LSTM(output_dim=hps[0], return_sequences=True),
                            input_shape=(config.max_review_length, 6),
                            merge_mode='concat'))
    model.add(Dropout(hps[1]))
    model.add(Bidirectional(LSTM(hps[2])))
    model.add(Dropout(hps[3]))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model


def multiple_rnn(hps):
    model = Sequential()
    model.add(LSTM(output_dim=32, return_sequences=True,
                                 input_shape=(config.max_review_length, 6)))
    model.add(Dropout(0.5))
    model.add(LSTM(32, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(32))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    return model


def calibrate_rnn():
    model = Sequential()
    model.add(LSTM(output_dim=4, return_sequences=True,
                            input_shape=(config.clibrate_length, 6)))
    model.add(Dropout(0.2))
    model.add(LSTM(20))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model

