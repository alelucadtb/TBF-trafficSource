import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path

def sourceModule(Ton, Toff, tau, B, L, Nc, namefile):
    # number of batches in a ON period
    z = math.floor(Ton / tau)
    # number of cycles that starts from zero and then should be increase
    ti = []
    for value in range(0, Nc + z*10000):
        for time in range(0, z):
            i = (Ton + Toff) * value + tau * time
            ti.append(i)
    # vector that represents the different batch sizes
    Bi = np.random.geometric(p = 1/B, size = len(ti))

    # initialize the matrix S
    S = []
    # given in the assignment
    rows = Nc * (math.floor(Ton / tau) + 1)
    colums = 3
    for rw in range(0, rows):
        a = []
        for cl in range(0, colums):
            if cl == 0:
                if rw == 0:
                    a.append(0)
                else:
                    a.append(ti[rw] - ti[rw-1])
            elif cl == 1:
                a.append(Bi[rw])
            else:
                a.append(Bi[rw] * L)
        S.append(a)
    # print the result in a file
    mat = np.matrix(S)
    with open(namefile ,'wb') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.2f')

def labeling(capacity, element, vector):
    if capacity - element >= 0:
        capacity = capacity - element
        vector.append(1)
    else:
        vector.append(0)
    return capacity

def checkingTime(time, element, capacity, rho, b):
    if time + element < 1:
        time = time + element
    else:
        time = time + element - int(element)
        add = rho * int(element)
        if capacity + add < b:
            capacity = capacity + add
        else:
            capacity = b
    return time, capacity


def tokenBucketFilter(namefile, rho, b, b0):
    mat = np.loadtxt(namefile , delimiter=' ')
    capacity = b0
    # it is a sufficient high value
    elm0prev = 10000000
    time = 0
    # column vector in which it is stored the result
    F = []

    for elm in mat:
        # elm[0] is the arrival time
        # elm[1] is the batch size --> number of packets for an arrival
        # elm[2] is the aggregated workload 
        if elm[0] <= elm0prev:
            # print(capacity)
            for num in range(0, int(elm[1])):
                # check for every packet
                capacity = labeling(capacity, elm[2]/elm[1], F)
            time, capacity = checkingTime(time, elm[0], capacity, rho, b)
            # print(capacity)
        else:
            # print(capacity)
            time, capacity = checkingTime(time, elm[0], capacity, rho, b)
            # print(capacity)
        elm0prev = elm[0]

    for element in F:
        print(element)



sourceModule(1, 1, 0.2, 3, 1000, 10000, 'output.txt')
tokenBucketFilter('output.txt', 8000, 3000, 3000)