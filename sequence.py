from DSU import DSU
import numpy as np
import math

EPS = 10**(-9)
TH, MUL = 15000, 10**10

def getDistanceBetweenBox(box1, box2):
    x1Min, y1Min, x1Max, y1Max = box1[0], box1[1], box1[2], box1[3]
    x2Min, y2Min, x2Max, y2Max = box2[0], box2[1], box2[2], box2[3]
    if x2Max <= x1Min:
        if y2Min > y1Max:
            return getDistance(x1Min, y1Max, x2Max, y2Min)
        elif y2Max < y1Min:
            return getDistance(x1Min, y1Min, x2Max, y2Max)
        else:
            return float("inf")
    elif x1Max <= x2Min:
        if y2Min > y1Max:
            return getDistance(x1Max, y1Max, x2Min, y2Min)
        elif y2Max < y1Min:
            return getDistance(x1Max, y1Min, x2Min, y2Max)
        else:
            return float("inf")
    else:
        if y2Min >= y1Max:
            return y2Min - y1Max
        elif y2Max <= y1Min:
            return y1Min - y2Max
        else:
            return getDistance((x1Min + x1Max) / 2, (y1Min + y1Max) / 2, (x2Min + x2Max) / 2, (y2Min + y2Max) / 2)
        
def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def connectivityStrength(yd, C):
    return MUL / (((yd + EPS) ** 2) * (C + EPS))

# CSF[i, j] shows the connectivity strength between the 
# connected components i and j, so if its less than a 
# threshold value, two componenets dont belong to the 
# same sequence and otherwise they does 
def arrange(contours, centroids):
    global TH
    n = len(contours)
    C = np.zeros([n, n])
    CSF = np.zeros([n, n])
    
    V = sorted([(contours[i], i) for i in range(len(contours))], 
               key=lambda x : getDistance(0, 0, centroids[x[1]][0], centroids[x[1]][1]))
    dsu = DSU(len(V))

    for i in range(n):
        for j in range(n):
            if i == j:
                C[i][j] = 0
                continue
            C[i][j] = getDistanceBetweenBox(contours[i], contours[j])
                
    for i in range(n):
        C1x = centroids[i][0]
        for j in range(n):
            C2x = centroids[j][0]
            yd = abs(C2x - C1x)
            CSF[i][j] = connectivityStrength(yd, C[i][j])
    
    
    for _ in range(len(V)):
        i = V[_][1]
        maxCSF, j = 0, -1
        # print(f"finding CC for {i}")
        for temp_ind in range(_, n):
            ind = V[temp_ind][1]
            # print(f"checking CC {ind} csf = {CSF[i][ind]}")
            if CSF[i][ind] <= TH + 10**3:
                continue
            if CSF[i][ind] > maxCSF and ind != i:
                maxCSF = CSF[i][ind]
                j = ind

        if j != -1:
            dsu.union(j, i)
            # print(f"merging {i} with {j} csf = {maxCSF}, parent = {dsu.find(i)}, {dsu.find(j)}")
            # dsu.printDSU()
        else:
            pass
            # print("didn't find anything...")

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

    return lines