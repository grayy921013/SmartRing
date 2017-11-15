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
char = name.upper()
if not os.path.exists(char):
    os.makedirs(char)


class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.f = None
        self.quit = False

    def run(self):
        while not self.quit:
            data = ser.readline().decode("utf-8")
            if self.f:
                f.write(data)

    def pause(self):
        self.f = None

    def kill(self):
        self.quit = True

i = 0
t = WorkerThread()
t.start()

while i < 25:
    input("#" + str(i) + " ready? ")
    f = open(char + "/" + str(datetime.now()), "w+")
    t.f = f
    input("finish?")
    print("Goodbye!")
    t.f.close()
    t.pause()
    i += 1
t.kill()
