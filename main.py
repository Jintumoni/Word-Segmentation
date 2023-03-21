import cv2 as cv
from connected_component import connected_components
from distanceTransform import DT
from sequence import arrange

# step 1. loading the image
img = cv.imread('./photos/skew.png');
H, W = img.shape[0], img.shape[1]


# step 2. convert the image to grayslace by 
#         selecting a threshold, all the pixels values 
#         greater than the threshold is set to 255 and others to 0
gray_scale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
(thresh, BnW_image) = cv.threshold(gray_scale, 200, 255, cv.THRESH_BINARY)


# step 3. apply distance transform (DT)
distTransform = DT(BnW_image)
_, final_img = cv.threshold(distTransform, 10, 255, cv.THRESH_BINARY)

# step 4. apply BFS to find contour
contours = connected_components(final_img)
for contour in contours:
    color = (0, 0, 0) # black boxes
    cv.rectangle(img, (contour[1], contour[0]), (contour[3], contour[2]), color, thickness=1)

lines = arrange(contours)
for _ in range(len(lines)):
    for i in range(0, len(lines[_]) - 1):
        box1, box2 = lines[_][i], lines[_][i + 1]
        startPoint = (box1[1] + box1[3]) // 2, (box1[0] + box1[2]) // 2 
        endPoint = (box2[1] + box2[3]) // 2, (box2[0] + box2[2]) // 2
        color = (0, 255, 0)
        thickness = 3
        cv.line(img, startPoint, endPoint, color, thickness=thickness)

cv.imshow('distance transform', distTransform)
cv.imshow('transformed image', final_img)
cv.imshow('contours', img)

cv.waitKey(0)
cv.destroyAllWindows()
