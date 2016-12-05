import os
import cv2
import dlib
import numpy as np
#检测所有的人脸数据。人脸图片大小为256*256。

def get_all_image(filepath):
    #读取每个目录下的所有图片
    pathDir = os.listdir(filepath)
    fileList=[]
    for allDir in pathDir:
        child  = os.path.join('%s\%s' % (filepath, allDir))
        fileList.append(child)
    fileList.sort(key=lambda x: int(x[x.index("img") + 3:-4]))
    return fileList

def get_face(filename):
    #检测人脸
    im=cv2.imread(filename)

    detector = dlib.get_frontal_face_detector()
    rect = detector(im, 1)[0]
    face=im[rect.top(): rect.bottom(),rect.left():rect.right()]

    face=cv2.resize(face,(256,256))

    return face

def save_image(all_image_path,filename):
    #保存图片
    length=len(all_image_path)

    dst=np.zeros((length,256*256))
    i=0
    for path in all_image_path:

        print(path)

        face=get_face(path)

        if not os.path.exists(".\\colorface\\"+'\\'.join(path.split('\\')[4:-1])):
            os.makedirs(".\\colorface\\"+'\\'.join(path.split('\\')[4:-1]))
        cv2.imwrite(".\\colorface\\"+'\\'.join(path.split('\\')[4:]),face)#将彩色人脸图片保存到./colorface
        grayface=cv2.cvtColor(face,cv2.COLOR_RGB2GRAY)
        if not os.path.exists(".\\grayface\\"+'\\'.join(path.split('\\')[4:-1])):
            os.makedirs(".\\grayface\\"+'\\'.join(path.split('\\')[4:-1]))
        cv2.imwrite(".\\grayface\\" +'\\'.join(path.split('\\')[4:]), grayface)  # 将黑白人脸图片保存到./grayface

        dst[i,:]=grayface.reshape(-1)
        i+=1
    np.save(".\\data\\"+filename,dst)#将视频图片保存到./data
    print(filename+" done")
    return dst

def get_dir():
    #读取dir.txt中的目录
    p=[]
    with open("dir.txt","r") as f:
        for line in f.readlines():
            p.append(line)
    return p


if __name__ == "__main__":
    all_dir=get_dir()
    for p in all_dir:
        p=p.strip()
        all_image=get_all_image(p)
        filename = p.split("\\")[-2]+p.split("\\")[-1]
        print(filename)
        save_image(all_image,filename)


