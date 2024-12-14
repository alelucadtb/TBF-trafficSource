import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path

def sourceModule(Ton, ToffMean, tau, B, L, Nc, namefile):
    # number of batches in a ON period
    Toff = np.random.exponential(scale = ToffMean)
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
remove the tokens in the TBF corresponding to the bits in a packet.
For labeling the packets:
- 1 if they are compliant
- 0 if they are excess
'''
def labeling(capacity, element, vector):
    if capacity - element >= 0:
        capacity = capacity - element
        vector.append(1)
    else:
        vector.append(0)
    return capacity

'''
tokens are generated throw the time. 
If the token rate is 8000 token/s, they aren't generated as a block of 8000 tokens every second.
'''
def tokenGeneration(element, rate, capacity, b):
    capacity = min(capacity + element * rate, b)
    return capacity

def compliantPackets(vector):
    sum = 0
    for element in vector:
        if element == 1:
            sum = sum + 1
    return sum/len(vector)
    
def tokenBucketFilter(namefile, rho, b, b0):
    mat = np.loadtxt(namefile , delimiter=' ')
    capacity = b0
    # column vector in which it is stored the result
    F = []

    for elm in mat:
        '''
        different elements of elm mean:
        - elm[0] is the arrival tisme
        - elm[1] is the batch size --> number of packets for an arrival
        - elm[2] is the aggregated workload 
        '''
        # print (elm[0], int(elm[1]), int(elm[2]), sep = ' ')
        # the first things to do update the capacity of the TBF
        capacity = tokenGeneration(elm[0], rho, capacity, b)
        # check for every packet in a batch
        for num in range(0, int(elm[1])):
            capacity = labeling(capacity, int(elm[2])/int(elm[1]), F)
            # print(capacity)

    print("Compliant packets: ", compliantPackets(F))



sourceModule(1, 1, 0.2, 3, 1000, 10000, 'outputSource.txt')
tokenBucketFilter('outputSource.txt', 8000, 3000, 3000)