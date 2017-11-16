import os

for data in ["raw", "round", "scale"]:
    for lstm1 in [1, 2, 4, 6, 8, 16]:
        for dropout1 in [x * 0.1 for x in range(0, 10)]:
            for lstm2 in [20, 40, 60, 80, 100, 150, 200, 300]:
                for dropout2 in [x * 0.1 for x in range(0, 10)]:
                    command = "python train.py " + data + " " + str(lstm1) + " " + str(dropout1) + " " + str(lstm2) + " " + str(dropout2)
                    os.system(command)