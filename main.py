import sys
import getopt
import cv2 as cv
from connected_component import connected_components
from distanceTransform import DT
from sequence import arrange


def main(argv, LineSegmentation: bool):
    # if you don't provide -d or -b flags, these will be the default values
    BnW_THRESHOLD = 200
    DT_THRESHOLD = 6
    filename = ""

    try:
        opts, args = getopt.getopt(argv, "b:d:")
        filename = args[0]
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-b':
            BnW_THRESHOLD = int(arg)
        elif opt == '-d':
            DT_THRESHOLD = int(arg)

    print(f"Doing Word Segmentation on \"{filename}\" ...")

    # step 1. loading the image
    img = cv.imread(f"./photos/{filename}")

    # step 2. convert the image to binary (black and white)
    gray_scale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    (thresh, BnW_image) = cv.threshold(
        gray_scale, BnW_THRESHOLD, 255, cv.THRESH_BINARY)

    # step 3. apply distance transform (DT)
    distTransform = DT(BnW_image)
    _, final_img = cv.threshold(
        distTransform, DT_THRESHOLD, 255, cv.THRESH_BINARY)

    # step 4. apply BFS to find contour
    contours, centroids = connected_components(final_img)

    # step 5. perform line segmentation
    if LineSegmentation:
        print(f"Doing Line Segmentation on \"{filename}\" ...")
        lines = arrange(contours, centroids)

        # to store the words in a folder for future usage
        cnt = 0
        wordImgList = []
        letterBgr = 0
        name = filename[0:0+len(filename)-4]
        for _ in range(len(lines)):
            for i in range(len(lines[_])):
                x, y, h, w = lines[_][i][0][0], lines[_][i][0][1], abs(
                    lines[_][i][0][0]-lines[_][i][0][2]), abs(lines[_][i][0][1]-lines[_][i][0][3])
                letterBgr = img[x:x+h, y:y+w]
                wordImgList.append(letterBgr)
                cv.imwrite(f"./result/{name}_" + str(cnt) + ".png", letterBgr)
                cnt = cnt+1

        # to create the joining lines between the boxes and write the indexes of the boxes
        for _ in range(len(lines)):
            for i in range(0, len(lines[_]) - 1):
                box1, box2 = lines[_][i][0], lines[_][i + 1][0]
                startPoint = (box1[1] + box1[3]) // 2, (box1[0] + box1[2]) // 2
                endPoint = (box2[1] + box2[3]) // 2, (box2[0] + box2[2]) // 2
                color = (0, 255, 0)
                thickness = 3
                cv.line(img, startPoint, endPoint, color, thickness=thickness)

            for i in range(len(lines[_])):
                box1, msg = lines[_][i][0], str(lines[_][i][1])
                x, y = (box1[1] + box1[3]) // 2, (box1[0] + box1[2]) // 2
                font = cv.FONT_HERSHEY_SIMPLEX
                cv.putText(img, msg, (x, y), font, 1,
                           (0, 0, 255), 3, cv.LINE_AA)

        # to create the bounding boxes
        for contour in contours:
            color = (0, 0, 0)  # black boxes
            cv.rectangle(img, (contour[1], contour[0]),
                         (contour[3], contour[2]), color, thickness=1)

    # Scaling the image
    scale_percent = 50 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
 
    cv.imshow('Binarised Image', BnW_image)
    cv.imshow('Distance transform', distTransform)
    cv.imshow('Transformed image', final_img)
    cv.imshow('Word Segmentation', resized)

    print("Press any key to quit ...")

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv[1:], True)
