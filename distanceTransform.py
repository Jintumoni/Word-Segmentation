import numpy as np


def DT(binary_image):
    distances = np.zeros_like(binary_image, dtype=np.uint8)
    distances = 255 - distances
    height, width = binary_image.shape

    for i in range(height):
        for j in range(width):
            if binary_image[i, j] == 0:
                distances[i, j] = 0
            else:
                if i - 1 >= 0 and j - 1 >= 0:
                    distances[i, j] = min(
                        distances[i, j], distances[i-1, j-1] + 1)
                if i - 1 >= 0 and j >= 0:
                    distances[i, j] = min(
                        distances[i, j], distances[i-1, j] + 1)
                if i >= 0 and j - 1 >= 0:
                    distances[i, j] = min(
                        distances[i, j], distances[i, j - 1] + 1)
                if i - 1 >= 0 and j + 1 < width:
                    distances[i, j] = min(
                        distances[i, j], distances[i-1, j+1] + 1)
    return distances
