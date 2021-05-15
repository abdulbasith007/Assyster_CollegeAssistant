from django.shortcuts import render
import cv2
import numpy as np
from PIL import Image
from . import cvsupport
from assyster_app.models import Students,Tests,StudentResult

from django.contrib import messages


#########################################


heightImg = 700
widthImg  = 700
questions=5
choices=5
ans= [1,2,1,2,4]


#########################################


def upload_answer_sheet(request,test_id,student_id):
    if request.method!="POST":
        return render(request,"assyster_app/staff_template/upload_answer_sheet.html")
    img=request.FILES.get('pic')
    img = cv2.imdecode(np.fromstring(request.FILES['pic'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    #print(type(img))
    #print(type(np.array(img)))
    #print(type(np.asarray(img)))
    #img=np.array(img)
    print(type(img))
    
    img = cv2.resize(img, (widthImg, heightImg))

    
    ##############################################################
        
    imgFinal = img.copy()
    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
    imgCanny = cv2.Canny(imgBlur,10,70) # APPLY CANNY 



    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
    rectCon = cvsupport.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
    biggestPoints= cvsupport.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
    gradePoints = cvsupport.getCornerPoints(rectCon[1]) # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE

        
    if biggestPoints.size != 0 and gradePoints.size != 0:

    # BIGGEST RECTANGLE WARPING
        biggestPoints=cvsupport.reorder(biggestPoints) # REORDER FOR WARPING
        cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE

                # SECOND BIGGEST RECTANGLE WARPING
        cv2.drawContours(imgBigContour, gradePoints, -1, (255, 0, 0), 20) # DRAW THE BIGGEST CONTOUR
        gradePoints = cvsupport.reorder(gradePoints) # REORDER FOR WARPING
        ptsG1 = np.float32(gradePoints)  # PREPARE POINTS FOR WARP
        ptsG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])  # PREPARE POINTS FOR WARP
        matrixG = cv2.getPerspectiveTransform(ptsG1, ptsG2)# GET TRANSFORMATION MATRIX
        imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150)) # APPLY WARP PERSPECTIVE

                # APPLY THRESHOLD
        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
        imgThresh = cv2.threshold(imgWarpGray, 170, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE


        boxes = cvsupport.splitBoxes(imgThresh) # GET INDIVIDUAL BOXES
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

    stackedImage = cvsupport.stackImages(imageArray,0.5,lables)
    cv2.imshow("Result",stackedImage)
    ################################################################

    #cv2.imshow('Result',img)
    cv2.waitKey(0)
    #img = img.astype(np.uint8)
    #print(type(img))
    print("DONE")
    #print(request.user.students)           Doesnt work
    stud=Students.objects.filter(pk=student_id).first()
    #saving marks to database
    test=Tests.objects.filter(pk=test_id).first()
    try:
        
        studRes=StudentResult(student_id=stud,marks=score,test_id=test)
        studRes.save()
    except Exception as e:
        print("######################")
        print(e)
        messages.error(request,"Failed")
        test=Tests.objects.filter(pk=test_id).first()
        print(test)
        print(test.subject_id.course_id)
        students=Students.objects.filter(course_id=test.subject_id.course_id)
        
        print(students)
        return render(request,"assyster_app/staff_template/test_details.html",{"test":test,"students":students})
    #Returning to prev page
    #test=Tests.objects.filter(pk=test_id).first()
    print(test)
    print(test.subject_id.course_id)
    students=Students.objects.filter(course_id=test.subject_id.course_id)
    
    print(students)
    messages.success(request,"Operation Successfull,         Marks Scored ( In % ) : {0}".format(score))
    return render(request,"assyster_app/staff_template/test_details.html",{"test":test,"students":students})
