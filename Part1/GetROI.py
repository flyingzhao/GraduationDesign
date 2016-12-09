import cv2
import dlib
import numpy as np


predictor = dlib.shape_predictor("../model/dlib/shape_predictor_68_face_landmarks.dat")

bgr=cv2.imread("./align_face/sub03/EP19_08\img60.jpg")
rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)


points=predictor(rgb,dlib.rectangle(0,0,256,256))

result=list(map(lambda p: (p.x, p.y), points.parts()))

cv2.imshow("a",bgr)
for i in range(68):
    if result[i][0]>0 and result[i][1]>0:
        cv2.circle(bgr,(result[i][0],result[i][1]),1, (255,0,0))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(bgr, str(i+1), (result[i][0],result[i][1]), font,0.3, (255, 255, 255))

cv2.rectangle(bgr,(result[17][0],result[19][1]),(result[21][0],result[41][1]),(255,0,0))
cv2.rectangle(bgr,(result[22][0],result[24][1]),(result[26][0],result[46][1]),(255,0,0))
cv2.rectangle(bgr,(result[48][0],result[50][1]),(result[54][0],result[57][1]),(255,0,0))

cv2.imshow("b",bgr)
#
cv2.imshow("c",bgr[result[19][1]-5:result[41][1]+5,result[17][0]-5:result[21][0]+5])
cv2.imshow("d",bgr[result[24][1]-5:result[46][1]+5,result[22][0]-5:result[26][0]+5])
cv2.imshow("e",bgr[result[50][1]-5:result[57][1]+5,result[48][0]-5:result[54][0]+5])

cv2.waitKey(0)
