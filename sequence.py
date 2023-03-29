from DSU import DSU
import numpy as np
import math

EPS = 10**(-9)

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def getDistanceBetweenBox(box1, box2):
    x1Min, y1Min, x1Max, y1Max = box1[0], box1[1], box1[2], box1[3]
    x2Min, y2Min, x2Max, y2Max = box2[0], box2[1], box2[2], box2[3]

    if x2Max < x1Min:
        # box1 below box2
        if y2Min > y1Max:
            # box1 on left
            return getDistance(x1Min, y1Max, x2Max, y2Min)
        elif y2Max < y1Min:
            # box1 on right
            return getDistance(x1Min, y1Min, x2Max, y2Max)
        else:
            # box1 in-between
            return x1Min - x2Max
    elif x1Max < x2Min:
        # box1 above box2
        if y2Min > y1Max:
            # box1 on left
            return getDistance(x1Max, y1Max, x2Min, y2Min)
        elif y2Max < y1Min:
            # box1 on right
            return getDistance(x1Max, y1Min, x2Min, y2Max)
        else:
            # box1 in-between
            return x2Min - x1Max
    else:
        if y2Min >= y1Max:
            # box1 on left (parallel)
            return y2Min - y1Max
        elif y2Max <= y1Min:
            # box1 on right (parallel)
            return y1Min - y2Max
        else:
            # overlap
            return 0

def getSlope(x1, y1, x2, y2):
    slope = (x2 - x1) / (y2 - y1 + EPS)
    return abs(math.atan(slope)) * 180 / math.pi

def getSlopeFactor(slope):
    return 50 * math.exp(-slope * slope / 150)

def getDistanceFactor(distance):
    return -pow(distance, 2) / 1000 + 50

def connectivityStrength(x1, y1, x2, y2, D):
    slope = getSlope(x1, y1, x2, y2)
    slopeFactor = getSlopeFactor(slope)
    distanceFactor = getDistanceFactor(D)
    CSF = distanceFactor + slopeFactor
    return CSF - 50


def lineCorrection(line, CSF):
    correction = []
    line = sorted(line, key=lambda x: (x[0][1] + x[0][3]) / 2)
    print('\n before correction')
    for l in line:
        print(l[1], end=' ')
    for l in line:
        maxCSF, ind = 0, -1
        for i in range(len(correction)):
            if CSF[correction[i][-1][1]][l[1]] - EPS > maxCSF:
                maxCSF = CSF[correction[i][-1][1]][l[1]]
                ind = i

        if ind == -1:
            correction.append([l])
        else:
            correction[ind].append(l)
    
    print('\nafter correction')
    for l in correction:
        for line in l:
            print(line[1], end=' ')
        print('\n')
    return correction

def arrange(contours, centroids):
    n = len(contours)
    C = np.zeros([n, n])
    CSF = np.zeros([n, n])
    # CSF[i, j] shows the connectivity strength between the connected components i and j
    slope = np.zeros([n, n])

    V = sorted([(contours[i], i) for i in range(len(contours))],
               key=lambda x: getDistance(0, 0, centroids[x[1]][0], centroids[x[1]][1]))
    dsu = DSU(len(V))

    for i in range(n):
        for j in range(n):
            C[i][j] = getDistanceBetweenBox(contours[i], contours[j])
            slope[i][j] = getSlope(centroids[i][0], centroids[i][1], centroids[j][0], centroids[j][1])
            # C[i][j] = getDistance(centroids[i][0], centroids[i][1], centroids[j][0], centroids[j][1])
            CSF[i][j] = connectivityStrength(
                centroids[i][0], centroids[i][1], centroids[j][0], centroids[j][1], C[i][j])

    for _ in range(len(V)):
        i = V[_][1]
        maxCSF, j = 0, -1
        print(
            f"finding CC for {i}")
        for temp_ind in range(max(_ - 40, 0), min(_ + 40, n)):
            ind = V[temp_ind][1]
            print(
                f"checking CC {ind}, csf = {CSF[i][ind]}, dis = {C[i][ind]}, slope = {slope[i][ind]}")
            # skip the ind_th box if it lies on the left side of i_th box
            if contours[ind][3] < contours[i][3]:
                continue

            if CSF[i][ind] > maxCSF and ind != i:
                maxCSF = CSF[i][ind]
                j = ind

        if j != -1:
            dsu.union(j, i)
            print(
                f"merging {i} with {j} csf = {maxCSF}, parent = {dsu.find(i)}, {dsu.find(j)}")
            # dsu.printDSU()
        else:

            print("didn't find anything...")

    # print(f"no of lines = {dsu.distinctParents()}")
    lines = [[] for _ in range(dsu.distinctParents())]
    indexDictionary = {}
    curr = 0

    for _ in range(len(V)):
        i = V[_][1]
        root = dsu.find(i)
        if root in indexDictionary:
            index_of_root = indexDictionary[root]
        else:
            index_of_root = indexDictionary[root] = curr
            curr += 1

        lines[index_of_root].append(V[_])
    
    correctedLines = []
    for line in lines:
        for lines in lineCorrection(line, CSF):
            correctedLines.append(lines)

    return correctedLines

