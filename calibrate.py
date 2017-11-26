#!/usr/local/bin/python3
import serial

import threading
import time
import config

class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.lock = threading.RLock()
        self.ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
        self.running = True
        self.data = ''

    def run(self):
        while self.running:
            self.lock.acquire()
            self.data = self.ser.readline().decode("utf-8")
            self.lock.release()

    def pause(self):
        self.lock.acquire()
        self.lock.release()

    def kill(self):
        print("kill")
        self.running = False

    def get_date(self):
        self.lock.acquire()
        data = self.data
        self.lock.release()
        return data


def work(ser):
    t = WorkerThread()
    t.start()
    i = 0
    stage = 'gravity'
    times = 20
    true_grav = 16384
    grav_range = 200
    buf = []
    while True:
        data = t.get_date().strip().split(',')
        if i % 5 == 0:
            ring_pos = ':)'
            if true_grav - grav_range > int(data[2]) < true_grav + grav_range:
                ring_pos = ':('
            print(ring_pos)
            i = 0
        i += 1

        finished = True
        if stage == 'gravity':
            grav = int(data[2])
            buf.append(grav)
            if len(buf) == times:
                for g in buf:
                    if true_grav - grav_range > g < true_grav + grav_range:
                        finished = False
                if finished:
                    stage = '1'
                buf = []
        elif stage == '1':
            print('FINISHED')
            return True

def print_data():
    ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
    while True:
        data = ser.readline().decode("utf-8")
        print(data)



if __name__ == '__main__':
    ser = serial.Serial(config.port, 9600)
    #work(ser)
    print_data()