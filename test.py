import config
import data
from keras.models import load_model
import numpy as np
import serial
import threading
import config
from keras.preprocessing import sequence

model = load_model('model_default.new.model')
X, Y = data.get_from_folder(dir="zhehui")
print(X)
print(model.evaluate(X, Y))

