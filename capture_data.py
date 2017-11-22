#!/usr/local/bin/python3
import serial

import os
from datetime import datetime
import threading
import time

lock = threading.RLock()

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
        self.ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
        self.running = True

    def run(self):
        while self.running:
            data = self.ser.readline().decode("utf-8")
            lock.acquire()
            if self.f:
                f.write(data)
            lock.release()

    def pause(self):
        lock.acquire()
        self.f.close()
        self.f = None
        lock.release()

    def kill(self):
        print ("kill")
        self.running = False

    def set_file(self, f):
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