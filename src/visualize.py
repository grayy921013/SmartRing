import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join

mypath = "../8"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

x = []
acc_x = []
acc_y = []
acc_z = []
gyro_x = []
gyro_y = []
gyro_z = []

index = 0
file_index = 1
total_index = 10
for file_name in onlyfiles:
    with open(mypath+'/'+file_name) as f:
        content = f.readline().strip()
        while content:
            content = content.split(',')
            x.append(index)
            acc_x.append(int(content[0]) / -300)
            acc_y.append(int(content[1]) / -300)
            acc_z.append(int(content[2]) / 300)
            gyro_x.append(int(content[3]) / 500)
            gyro_y.append(int(content[4]) / 500)
            gyro_z.append(int(content[5]) / 500)
            index += 1
            content = f.readline().strip()
    plt.subplot(6, 1, 1)
    plt.plot(x, acc_x, '.-')
    plt.ylabel('acc x')
    plt.xlim(0, 50)
    plt.ylim(-100,100)

    plt.subplot(6, 1, 2)
    plt.plot(x, acc_y, '.-')
    plt.ylabel('acc y')
    plt.xlim(0, 50)
    plt.ylim(-100,100)

    plt.subplot(6, 1, 3)
    plt.plot(x, acc_z, '.-')
    plt.ylabel('acc z')
    plt.xlim(0, 50)
    plt.ylim(-100,100)

    plt.subplot(6, 1, 4)
    plt.plot(x, gyro_x, '.-')
    plt.ylabel('gyro x')
    plt.xlim(0, 50)
    plt.ylim(-50,50)

    plt.subplot(6, 1, 5)
    plt.plot(x, gyro_y, '.-')
    plt.ylabel('gyro y')
    plt.xlim(0, 50)
    plt.ylim(-50,50)

    plt.subplot(6, 1, 6)
    plt.plot(x, gyro_z, '.-')
    plt.ylabel('gyro z')
    plt.xlim(0, 50)
    plt.ylim(-50,50)
    plt.show()

    index = 0
    x = []
    acc_x = []
    acc_y = []
    acc_z = []
    gyro_x = []
    gyro_y = []
    gyro_z = []