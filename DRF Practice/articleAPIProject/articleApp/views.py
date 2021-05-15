from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import articleSerializer,MarksSerializer,ImageSerializer
from .models import Articles
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json

#graph imports
import matplotlib.pyplot as plt
import numpy as np
from .custom_renderers import JPEGRenderer,PNGRenderer
from wsgiref.util import FileWrapper

#openCV imports
import cv2
import numpy as np
from PIL import Image
from . import cvsupport
#################################
heightImg = 700
widthImg  = 700
questions=5
choices=5
#ans= [1,2,0,2,4]
#################################


class omr(APIView):
    def get(self, request):
        image = request.FILES["image"]
        img = cv2.imdecode(np.fromstring(request.FILES['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (widthImg, heightImg))
        data = json.loads(request.data["data"])
        print(data['ans'])
        ans=data['ans']         #List of correct answers


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
        lables = [["Original","Gray","Edges","Contours"],["Biggest Contour","Threshold","Warpped","Blank"]]

        stackedImage = cvsupport.stackImages(imageArray,0.5,lables)
        cv2.imshow("Result",stackedImage)
        ################################################################

        #cv2.imshow('Result',img)
        cv2.waitKey(0)
        #img = img.astype(np.uint8)
        #print(type(img))
        print("DONE")

        ######################################
        dct=dict()
        dct['marks']=score
        return Response(dct,status=status.HTTP_201_CREATED)

#class gimg works perfectly fine and is ready to be merged
class gimg(APIView):

    renderer_classes = [JPEGRenderer]

    def get(self,request):

        sl=MarksSerializer(data=request.data)
        if sl.is_valid():
            print(sl.data)
            print(type(sl.data))
        else:
            print("Skpped")
        mrks=list(sl.data['arr'])
        x_axis=[]
        for i in range(0,len(mrks)):
            x_axis.append(i+1)
        x=np.array(x_axis)
        y=np.array(mrks)
        plt.switch_backend('agg')
        #RuntimeError: main thread is not in main loop...to solve this error
        plt.plot(x,y)
        plt.xlabel('Semester')
        plt.ylabel('Marks')
        plt.title('Marks analysis')
        plt.grid(True)
        plt.savefig("test.png")
        print(type(plt))
        #plt.show()
        file = open("test.png", 'rb')
        return Response(FileWrapper(file))































'''
@api_view(['GET'])
@renderer_classes([JPEGRenderer])
def gimg(request):
    x=np.array([1,2,3,4])
    y=np.array([1,4,9,16])
    plt.plot(x,y)
    plt.xlabel('x')
    plt.ylabel('x square')
    plt.title('square function')
    plt.grid(True)
    plt.savefig("test.png")
    print(type(plt))
    #plt.show()
    file = open("test.png", 'rb')
    return Response(FileWrapper(file))
'''
@api_view(['GET','POST'])
def home(request):
    if request.method=="GET":
        a=Articles.objects.all()
        s=articleSerializer(a,many=True)
        return Response(s.data)
    elif request.method=="POST":
        sl=articleSerializer(data=request.data)
        if(sl.is_valid()):
            sl.save()
            return Response(sl.data,status=status.HTTP_201_CREATED)
        return Response(sl.data,status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def specific(request,id):
    try:
        a=Articles.objects.get(id=id)
    except Articles.DoesNotExist:
        return HttpResponse(status=404)
    if request.method=="GET":
        sl=articleSerializer(a)
        return JsonResponse(sl.data)
    elif request.method=="PUT":
        data=JSONParser().parse(request)
        sl=articleSerializer(a,data=data)
        if sl.is_valid():
            sl.save()
            return JsonResponse(sl.data,status=201)
        return JsonResponse(sl.errors,status=400)
    if request.method=="DELETE":
        a.delete()
        return HttpResponse(status=201)

'''
@csrf_exempt
def home(request):
    if request.method=="GET":
        a=Articles.objects.all()
        s=articleSerializer(a,many=True)
        return JsonResponse(s.data,safe=False)
    elif request.method=="POST":
        data=JSONParser().parse(request)
        sl=articleSerializer(data=data)
        if sl.is_valid():
            sl.save()
            return JsonResponse(sl.data,status=201)
        return JsonResponse(sl.errors,status=400)
'''
'''
class home(APIView):
    def get(self,request):
        artcles=Articles.objects.all()
        srlzr=articleSerializer(artcles,many=True)
        return Response(srlzr.data)
'''


