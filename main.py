import cv2 as cv
from connected_component import connected_components
from distanceTransform import DT
from sequence import arrange

INF = float("inf")

# step 1. loading the image
img = cv.imread('./photos/p_dev_0005_copy.png');
H, W = img.shape[0], img.shape[1]


# step 2. convert the image to grayslace by 
#         selecting a threshold, all the pixels values 
#         greater than the threshold is set to 255 and others to 0
gray_scale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
(thresh, BnW_image) = cv.threshold(gray_scale, 200, 255, cv.THRESH_BINARY)


# step 3. apply distance transform (DT)
distTransform = DT(BnW_image)
_, final_img = cv.threshold(distTransform, 9, 255, cv.THRESH_BINARY)


cv.imshow('distance transform', distTransform)
cv.imshow('transformed image', final_img)

# step 4. apply BFS to find contour
contours = connected_components(final_img)

for contour in contours:
    color = (0, 0, 0) # black boxes
    cv.rectangle(img, (contour[1], contour[0]), (contour[3], contour[2]), color, thickness=1)

# CSF = arrange(contours)
# CSFThreshold = 0.001

# for i in range(len(CSF)):
#     for j in range(len(CSF)):
#         if CSF[i][j] >= CSFThreshold:
#             startPoint = (contours[i][1] + contours[i][3]) // 2, (contours[i][0] + contours[i][2]) // 2 
#             endPoint = (contours[j][1] + contours[j][3]) // 2, (contours[j][0] + contours[j][2]) // 2
#             color = (0, 255, 0)
#             thickness = 3
#             cv.line(img, startPoint, endPoint, color, thickness=thickness)

# # print(CSF)
cv.imshow('contours', img)
cv.waitKey(0)
cv.destroyAllWindows()