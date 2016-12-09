import os
import numpy as np
import cv2
import dlib
from scipy.stats import itemfreq
from skimage.feature import local_binary_pattern

predictor = dlib.shape_predictor("../model/dlib/shape_predictor_68_face_landmarks.dat")


def get_dir():
    #读取dir.txt中的目录
    p=[]
    with open("dir.txt","r") as f:
        for line in f.readlines():
            p.append(line)
    return p


def get_all_image(filepath):
    #读取每个目录下的所有图片
    pathDir = os.listdir(filepath)
    fileList=[]
    for allDir in pathDir:
        child  = os.path.join('%s\%s' % (filepath, allDir))
        fileList.append(child)
    fileList.sort(key=lambda x: int(x[x.index("img") + 3:-4]))
    return fileList


def get_roi_feature(file_name):

    bgr = cv2.imread(file_name)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    points = predictor(rgb, dlib.rectangle(0, 0, 256, 256))
    result = list(map(lambda p: (p.x, p.y), points.parts()))

    left_eye = bgr[result[19][1] - 5:result[41][1] + 5, result[17][0] - 5:result[21][0] + 5]
    right_eye = bgr[result[24][1] - 5:result[46][1] + 5, result[22][0] - 5:result[26][0] + 5]
    mouth = bgr[result[50][1] - 5:result[57][1] + 5, result[48][0] - 5:result[54][0] + 5]

    gray_left_eye=cv2.cvtColor(left_eye, cv2.COLOR_BGR2GRAY)
    gray_right_eye=cv2.cvtColor(right_eye, cv2.COLOR_BGR2GRAY)
    gray_mouth=cv2.cvtColor(mouth, cv2.COLOR_BGR2GRAY)

    radius = 1
    no_points = 8 * radius
    lbp_left_eye = local_binary_pattern(gray_left_eye, no_points, radius, method='default')
    lbp_right_eye = local_binary_pattern(gray_right_eye, no_points, radius, method='default')
    lbp_mouth = local_binary_pattern(gray_mouth, no_points, radius, method='default')

    hist_left_eye, _ = np.histogram(lbp_left_eye.flatten(), 256, [0, 256])
    hist_right_eye, _ = np.histogram(lbp_right_eye.flatten(), 256, [0, 256])
    hist_mouth, _ = np.histogram(lbp_mouth.flatten(), 256, [0, 256])

    left_eye_feature = hist_left_eye/np.sum(hist_left_eye)
    right_eye_feature = hist_right_eye / np.sum(hist_right_eye)
    mouth_feature = hist_mouth / np.sum(hist_mouth)

    all_feature = np.concatenate((left_eye_feature, right_eye_feature, mouth_feature))

    return all_feature.reshape(1, 768)

if __name__ == "__main__":

    all_dir = get_dir()

    for p in all_dir:
        p = p.strip()
        filename = p.split("\\")[-2] + p.split("\\")[-1]

        all_image = get_all_image("./align_face/"+p.split("\\")[-2] + "/"+ p.split("\\")[-1])

        feature_mat=np.zeros((len(all_image),768))

        i=0
        for path in all_image:
            feature_mat[i,:]=get_roi_feature(path)
            i+=1

        np.save("./feature/"+filename, feature_mat)
        print(filename+" done")
