from DSU import DSU
import numpy as np
import math

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

# CSF[i, j] shows the connectivity strength between the 
# connected components i and j, so if its less than a 
# threshold value, two componenets dont belong to the 
# same sequence and otherwise they does 
def arrange(contours):
    n = len(contours)
    C = np.zeros([n, n])
    CSF = np.zeros([n, n])
    EPS = 10**(-9)
    TH = -float("inf")
    V = sorted([(contours[i], i) for i in range(len(contours))], 
               key=lambda x : getDistance(0, 0, (x[0][0] + x[0][2]) / 2, (x[0][1] + x[0][3]) / 2))
    dsu = DSU(len(V))

    for i in range(n):
        C1x, C1y = (contours[i][0] + contours[i][2]) / 2, (contours[i][1] + contours[i][3]) / 2
        for j in range(n):
            C2x, C2y = (contours[j][0] + contours[j][2]) / 2, (contours[j][1] + contours[j][3]) / 2
            C[i][j] = getDistance(C1x, C1y, C2x, C2y)
    
    for i in range(n):
        C1x = (contours[i][0] + contours[i][2]) / 2
        for j in range(n):
            C2x = (contours[j][0] + contours[j][2]) / 2
            yd = abs(C2x - C1x)
            CSF[i][j] = abs(C[i][j] - yd) / (yd + EPS)
            if i != j:
                TH = min(TH, CSF[i][j])

    for _ in range(len(V)):
        i = V[_][1]

        if dsu.hasParent(i):
            continue
        else:
            maxCSF, j = TH, -1
            for ind in range(n):
                if CSF[i][ind] == 0:
                    continue
                if CSF[i][ind] > maxCSF and dsu.find(ind) == ind and ind != i:
                    maxCSF = CSF[i][ind]
                    j = ind

            if j != -1:
                dsu.union(i, j)

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

        lines[index_of_root].append(V[_][0])

    return lines
