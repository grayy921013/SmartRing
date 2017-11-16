import config
import data
from keras.models import load_model
import numpy as np
import serial
import threading

model_name = 'model_default.model'

ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
array = []

class WorkerThread(threading.Thread):
    def __init__(self, x):
        super(WorkerThread, self).__init__()
        self.collecting = False
        self.quit = False
        self.x = x
        self.lock = threading.Lock()

    def run(self):
        while True:
            data = ser.readline().decode("utf-8").strip().split(",")
            with self.lock:
                if self.collecting:
                    int_data = []
                    for p in data:
                        int_data.append(int(p))
                    self.x.append(int_data)
                if self.quit:
                    return

    def collect(self, should_collect):
        with self.lock:
            self.collecting = should_collect

    def kill(self):
        with self.lock:
            self.quit = True

    def clear(self):
        with self.lock:
            del self.x[:]

t = WorkerThread(array)
t.start()

while True:
    input(" ready? ")
    t.collect(True)
    input("finish?")
    print(array)
    t.collect(False)
    t.clear()

# model = load_model(model_name)
# res = model.predict_classes(x_test[0], batch_size=config.batch_size, verbose=0)
# print (res[0])