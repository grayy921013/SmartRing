import config
import data
from keras.models import load_model
import numpy as np
import serial
import threading
import config
from keras.preprocessing import sequence

model_name = 'model_default.model'

ser = serial.Serial(config.port, 9600)
class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.collecting = False
        self.quit = False
        self.x = []
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
            #del self.x[:]
            self.x = []

    def get_array(self):
        with self.lock:
            return np.asarray([self.x])

t = WorkerThread()
t.start()
model = load_model(model_name)

while True:
    input(" ready? ")
    t.collect(True)
    input("finish?")
    t.collect(False)
    X_test = t.get_array()
    print(X_test)
    X_test = sequence.pad_sequences(X_test, maxlen=config.max_review_length)
    print(X_test)
    res = model.predict_classes(X_test, batch_size=config.batch_size, verbose=0)
    print(res[0])
    prob = model.predict_proba(X_test)
    print(prob)
    t.clear()

