#!/usr/local/bin/python3
import serial

import os
from datetime import datetime
import threading


ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
name = input("Enter the character: ")
if len(name) != 1:
    print("wrong length")
    exit()
input_count = input("# of samples you want to collect: ")
count = int(input_count)
char = name.upper()
if not os.path.exists(char):
    os.makedirs(char)


class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.f = None
        self.quit = False
        self.lock = threading.Lock()

    def run(self):
        while True:
            data = ser.readline().decode("utf-8")
            with self.lock:
                if self.f:
                    f.write(data)
                if self.quit:
                    return

    def pause(self):
        with self.lock:
            self.f.close()
            self.f = None

    def kill(self):
        with self.lock:
            self.quit = True

    def set_file(self, f):
        with self.lock:
            self.f = f

i = 0
t = WorkerThread()
t.start()

while i < count:
    input("#" + str(i) + " ready? ")
    f = open(char + "/" + str(datetime.now()), "w+")
    t.set_file(f)
    input("finish?")
    print("Goodbye!")
    t.pause()
    i += 1
t.kill()
