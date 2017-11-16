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
    if hps is None:
        return default_model()
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
