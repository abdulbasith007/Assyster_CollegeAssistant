import cv2
import numpy as np
import try1support
from PIL import Image
############################

heightImg = 700
widthImg  = 700
questions=5
choices=5
ans= [1,2,0,2,4]

############################

img=cv2.imread("1.jpg")
print(img)
tmpimg=Image.open("1.jpg")
print("PILLLLOOOWWWW",tmpimg)
print(np.array(tmpimg))
print(type(np.array(tmpimg)))
img = cv2.resize(img, (widthImg, heightImg))

imgFinal = img.copy()
imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
imgCanny = cv2.Canny(imgBlur,10,70) # APPLY CANNY 



imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
rectCon = try1support.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
biggestPoints= try1support.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
gradePoints = try1support.getCornerPoints(rectCon[1]) # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE

        

if biggestPoints.size != 0 and gradePoints.size != 0:

# BIGGEST RECTANGLE WARPING
    biggestPoints=try1support.reorder(biggestPoints) # REORDER FOR WARPING
    cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
    pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE

            # SECOND BIGGEST RECTANGLE WARPING
    cv2.drawContours(imgBigContour, gradePoints, -1, (255, 0, 0), 20) # DRAW THE BIGGEST CONTOUR
    gradePoints = try1support.reorder(gradePoints) # REORDER FOR WARPING
    ptsG1 = np.float32(gradePoints)  # PREPARE POINTS FOR WARP
    ptsG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])  # PREPARE POINTS FOR WARP
    matrixG = cv2.getPerspectiveTransform(ptsG1, ptsG2)# GET TRANSFORMATION MATRIX
    imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150)) # APPLY WARP PERSPECTIVE

            # APPLY THRESHOLD
    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
    imgThresh = cv2.threshold(imgWarpGray, 170, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE


    boxes = try1support.splitBoxes(imgThresh) # GET INDIVIDUAL BOXES
    #cv2.imshow("Split Test ", boxes[3])
    countR=0
    countC=0
    myPixelVal = np.zeros((questions,choices)) # TO STORE THE NON ZERO VALUES OF EACH BOX
    for image in boxes:
        #cv2.imshow(str(countR)+str(countC),image)
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countR][countC]= totalPixels
        countC += 1
        if (countC==choices):
            countC=0
            countR +=1
    print(myPixelVal)

    myIndex=[]
    for x in range (0,questions):
        arr = myPixelVal[x]
        myIndexVal = np.where(arr == np.amax(arr))
        myIndex.append(myIndexVal[0][0])
        print("USER ANSWERS",myIndex)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
    grading=[]
    for x in range(0,questions):
        if ans[x] == myIndex[x]:
            grading.append(1)
        else:
            grading.append(0)
            print("GRADING",grading)
            score = (sum(grading)/questions)*100 # FINAL GRADE
            print("SCORE",score)



#imageArray = ([img,imgGray,imgCanny,imgContours],[imgBlank, imgBlank, imgBlank, imgBlank])
imageArray = ([img,imgGray,imgCanny,imgContours],[imgBigContour,imgThresh,imgWarpColored, imgBlank])

    # LABELS FOR DISPLAY
#lables = [["Original","Gray","Edges","Contours"],["Biggest Contour","Threshold","Warpped","Final"]]
lables = [["Original","Gray","Edges","Contours"],["Biggest Contour","Threshold","Warpped","Final"]]

stackedImage = try1support.stackImages(imageArray,0.5,lables)
cv2.imshow("Result",stackedImage)

#cv2.imshow("Original Image",img)
cv2.waitKey(0)