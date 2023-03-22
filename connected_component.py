from collections import deque
import numpy as np

def connected_components(img):
    INF = float("inf")
    q = deque() 
    H, W = img.shape[0], img.shape[1]
    vis = np.zeros((H, W), dtype=int)
    contours, centroids = [], []
    dir_x = [-1, 1, 0, 0, 1, -1, -1, 1]
    dir_y = [0, 0, -1, 1, 1, -1, 1, -1]
    for row in range(H):
        for col in range(W):
            if img[row][col] == 0 and not vis[row][col]:
                x_min, x_max, y_min, y_max = INF, -INF, INF, -INF
                vis[row][col] = 1
                q.append((row, col))
                points, Cx, Cy = 1, row, col
                while len(q):
                    x, y = q.popleft()
                    x_min = min(x_min, x)
                    x_max = max(x_max, x)
                    y_min = min(y_min, y)
                    y_max = max(y_max, y)
                    for i in range(4):
                        x_ = x + dir_x[i]
                        y_ = y + dir_y[i]
                        if x_ < 0 or x_ >= H or y_ < 0 or y_ >= W:
                            continue
                        if not vis[x_][y_] and img[x_][y_] == 0:
                            vis[x_][y_] = 1
                            q.append((x_, y_))
                            Cx += x_
                            Cy += y_
                            points += 1
                Cx /= points
                Cy /= points
                contours.append([x_min, y_min, x_max, y_max])
                centroids.append([Cx, Cy])
    return contours, centroids

def find_contours(img):
    INF = float("inf")
    
    H, W = img.shape[0], img.shape[1]
    vis = np.zeros((H, W), dtype=int)
    contours = []
    dir_x = [-1, 1, 0, 0]
    dir_y = [0, 0, -1, 1]
    
    def recursive_connected_component(x1, y1, x2, y2):
        x_min, y_min, x_max, y_max = x1, y1, x2, y2
        for row in range(x1, x2 + 1):
            for col in range(y1, y2 + 1):
                if img[row][col] == 0 and not vis[row][col]:
                    q = deque() 
                    vis[row][col] = 1
                    q.append((row, col))
                    while len(q):
                        x, y = q.popleft()
                        x_min = min(x_min, x)
                        x_max = max(x_max, x)
                        y_min = min(y_min, y)
                        y_max = max(y_max, y)
                        for i in range(4):
                            x_ = x + dir_x[i]
                            y_ = y + dir_y[i]
                            if x_ < 0 or x_ >= H or y_ < 0 or y_ >= W:
                                continue
                            if not vis[x_][y_] and img[x_][y_] == 0:
                                vis[x_][y_] = 1
                                q.append((x_, y_))
                    x1, y1, x2, y2 = recursive_connected_component(x_min, y_min, x_max, y_max)
                    x_min = min(x_min, x1)
                    x_max = max(x_max, x2)
                    y_min = min(y_min, y1)
                    y_max = max(y_max, y2)

        return (x_min, y_min, x_max, y_max)

    def bfs(row, col):
        q = deque() 
        vis[row][col] = 1
        q.append((row, col))
        x_min, x_max, y_min, y_max = INF, -INF, INF, -INF
        while len(q):
            x, y = q.popleft()
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)
            for i in range(4):
                x_ = x + dir_x[i]
                y_ = y + dir_y[i]
                if x_ < 0 or x_ >= H or y_ < 0 or y_ >= W:
                    continue
                if not vis[x_][y_] and img[x_][y_] == 0:
                    vis[x_][y_] = 1
                    q.append((x_, y_))

        return (x_min, y_min, x_max, y_max)
        
    for row in range(0, H):
        for col in range(0, W):
            if img[row][col] == 0 and not vis[row][col]:
                x_min, y_min, x_max, y_max = bfs(row, col)
                x1, y1, x2, y2 = recursive_connected_component(x_min, y_min, x_max, y_max)
                x_min = min(x_min, x1)
                y_min = min(y_min, y1)
                x_max = max(x_max, x2)
                y_max = max(y_max, y2)
                contours.append([x_min, y_min, x_max, y_max])
    return contours

                

