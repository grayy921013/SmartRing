#!/usr/local/bin/python3
import serial

import os
from datetime import datetime
import threading

'''
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
'''

serial = serial.Serial('/dev/cu.usbmodem1411', 9600)
i = 0
while True:
    data = serial.readline().decode("utf-8")
    #dataline = serial.readline()
    i += 1
    if i % 5 == 0:
        print(data)
        i = 0
