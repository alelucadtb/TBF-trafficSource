import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path

def sourceModule(Ton, Toff, tau, B, L, Nc, namefile):
    # number of batches in a ON period
    z = math.floor(Ton / tau)
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

'''
for labeling the packets:
- 1 if they are compiant
- 0 if they are excess
'''
def labeling(capacity, element, vector):
    if capacity - element >= 0:
        capacity = capacity - element
        vector.append(1)
    else:
        vector.append(0)
    return capacity

# for manage the variable time and the token bucket generation rate (rho)
def checkingTime(time, element, capacity, rho, b):
    if time + element < 1:
        time = time + element
    else:
        # how many tokens must be sum to the token bucket
        time = time + element
        add = rho * int(time)
        if capacity + add < b:
            capacity = capacity + add
        else:
            capacity = b
        time = time % 1   
    return time, capacity

def compliantPackets(vector):
    sum = 0
    for element in vector:
        if element == 1:
            sum = sum + 1
    return sum/len(vector)
    
def tokenBucketFilter(namefile, rho, b, b0):
    mat = np.loadtxt(namefile , delimiter=' ')
    capacity = b0
    # it is a sufficient high value
    time = 0.0
    # column vector in which it is stored the result
    F = []

    for elm in mat:
        '''
        different elements of elm mean:
        - elm[0] is the arrival time
        - elm[1] is the batch size --> number of packets for an arrival
        - elm[2] is the aggregated workload 
        '''
        # the first things to do is to checking the time
        time, capacity = checkingTime(time, elm[0], capacity, rho, b)
        for num in range(0, int(elm[1])):
            # check for every packet
            capacity = labeling(capacity, int(elm[2])/int(elm[1]), F)
            # print(capacity)

    for line in F:
        print(line)



sourceModule(1, 1, 0.2, 3, 1000, 10000, 'output.txt')
tokenBucketFilter('SourceTrafficTrace.txt', 8000, 3000, 3000)