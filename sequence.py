import numpy as np
import math
import heapq

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

# CSF[i, j] shows the connectivity strength between the 
# connected components i and j, so if its less than a 
# threshold value, two componenets dont belong to the 
# same sequence and otherwise they does 
def arrange(contours):
    n = len(contours)
    C, slope = np.zeros([n, n]), np.zeros([n, n])
    CSF = np.zeros([n, n])
    visited = np.zeros([n])
    EPS = 10**(-9)
    TH = 300

    for i in range(n):
        C1x, C1y = (contours[i][0] + contours[i][2]) / 2, (contours[i][1] + contours[i][3]) / 2
        for j in range(n):
            C2x, C2y = (contours[j][0] + contours[j][2]) / 2, (contours[j][1] + contours[j][3]) / 2
            C[i][j] = getDistance(C1x, C1y, C2x, C2y)
            slope[i][j] = (C2x - C1x) / (C2y - C1y + EPS)
    
    # for i in range(n):
    #     C1x, C1y = (contours[i][0] + contours[i][2]) / 2, (contours[i][1] + contours[i][3]) / 2
    #     for j in range(n):
    #         if C[i][j] > TH or abs(slope[i][j]) > 0.5:
    #             CSF[i][j] = 0
    #             continue
    #         C2x, C2y = (contours[j][0] + contours[j][2]) / 2, (contours[j][1] + contours[j][3]) / 2
    #         yd = abs(C2x - C1x)
    #         xd = abs(C2y - C1y)

    #         CSF[i][j] = abs(C[i][j] - yd) / (yd + EPS)

    boxes = [((contours[i][0] + contours[i][2]) / 2, i) for i in range(len(contours))]
    heapq.heapify(boxes)

    while len(boxes):
        _, id = heapq.heappop(boxes)
        visited[id] = 1
        for col in range(n):
            if col == id or visited[col]:
                continue
            if C[i][j] > TH or abs(slope[i][j]) > 0.5:
                continue


    return CSF
