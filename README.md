# Word Segmentation for Hindi Language 

## 1. About the Project

Handwritten character recognition is an important filed of Optical
Character Recognition (OCR). The recognition of handwritten
text in scripts is one of the major areas of research.

The proper word level segmentation of printed or handwritten text is an important preprocessing step for optical character recognition (OCR). It is noticed that the languages having cursive nature in writing make the segmentation problem much more complicated. Hindi is one of the well known language in India having this cursive nature in writing style. The main challenge in handwritten word segmentation is to handle the inherent variability in the writing style of different individuals.



## 2. How to run the code?

1. Clone the github repository

   ```git clone https://github.com/Jintumoni/Word-Segmentation-Final-Year-Project.git```

2. Create a folder named *Photos* where you will put all the handwritten texts for which you want to perform word segmentation

   ```mkdir photos```

3. Put all the handwritten texts in the *Photos* directory

4. To run the code (with image as *myFile.png*)

   ```bash coderunner.sh myFile.png```

## 3. Output


The code works in the following order
- Reading the image
- Converting the image to binary image (black and white)
- Perform Distance Transform on the image
- Apply BFS to find the bounding boxes and calculate centroids of the boxes with an weighted average approach
- Apply Line Segmentation algorithm 

![Binarised image](/Screenshots/binarised.png)

![Distance Transform](/Screenshots/distanceTransform.png)

![Applying Threshold](/Screenshots/transformed.png)

![Final Output](/Screenshots/finalOutput.png)