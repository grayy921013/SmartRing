from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import config

#
# this script is for defining different models for testing
#

def get_model(hps = None, TAG = None):
    if TAG is None:
        print ('use default model')
    if TAG is 'best':
        return best_model()
    if hps is None:
        return default_model()
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
