import numpy as np
import cv2
import os
# a=np.load("1.npy")
# a=np.uint8(a)
# img=a[1,:]
# cv2.imshow("1",img.reshape((48,48)))
# cv2.imwrite("./test/1.jpg",img)
# cv2.waitKey(0)
# b=np.load("./label/sub01EP03_02.npy")
# print(b.shape)
# print(b[0,130:161])
# a = np.load("./label/sub01EP04_03.npy")
#
# print(a)

#
# a=cv2.imread("F:/CASME2/CASME2_RAW/CASME2-RAW/sub01/EP02_01f/img1.jpg")
#
# cv2.imshow("b",a)
# H=np.array([[  4.07197868e-01 , -2.17464188e-02 , -6.33229053e+01],
#  [  1.55797074e-02  , 4.76993700e-01 , -9.89723085e+01]])
#
# img=cv2.warpAffine(a, H, (128, 128))
#
# cv2.imshow("a",img)
#
# cv2.waitKey(0)

# #
# bb=np.load("./align_data/bb/sub01EP03_02.npy")
# # print(a.shape)
#
# a=cv2.imread("F:/CASME2/CASME2_RAW/CASME2-RAW/sub01/EP02_01f/img1.jpg")
# cv2.imshow("a",a[bb[0,0]:bb[0,2],bb[0,1]:bb[0,3]])
# cv2.waitKey(0)