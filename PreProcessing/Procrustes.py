import os
import numpy as np
import cv2
"""Module for dlib-based alignment."""
TEMPLATE = np.float32([
    (0.0792396913815, 0.339223741112), (0.0829219487236, 0.456955367943),
    (0.0967927109165, 0.575648016728), (0.122141515615, 0.691921601066),
    (0.168687863544, 0.800341263616), (0.239789390707, 0.895732504778),
    (0.325662452515, 0.977068762493), (0.422318282013, 1.04329000149),
    (0.531777802068, 1.06080371126), (0.641296298053, 1.03981924107),
    (0.738105872266, 0.972268833998), (0.824444363295, 0.889624082279),
    (0.894792677532, 0.792494155836), (0.939395486253, 0.681546643421),
    (0.96111933829, 0.562238253072), (0.970579841181, 0.441758925744),
    (0.971193274221, 0.322118743967), (0.163846223133, 0.249151738053),
    (0.21780354657, 0.204255863861), (0.291299351124, 0.192367318323),
    (0.367460241458, 0.203582210627), (0.4392945113, 0.233135599851),
    (0.586445962425, 0.228141644834), (0.660152671635, 0.195923841854),
    (0.737466449096, 0.182360984545), (0.813236546239, 0.192828009114),
    (0.8707571886, 0.235293377042), (0.51534533827, 0.31863546193),
    (0.516221448289, 0.396200446263), (0.517118861835, 0.473797687758),
    (0.51816430343, 0.553157797772), (0.433701156035, 0.604054457668),
    (0.475501237769, 0.62076344024), (0.520712933176, 0.634268222208),
    (0.565874114041, 0.618796581487), (0.607054002672, 0.60157671656),
    (0.252418718401, 0.331052263829), (0.298663015648, 0.302646354002),
    (0.355749724218, 0.303020650651), (0.403718978315, 0.33867711083),
    (0.352507175597, 0.349987615384), (0.296791759886, 0.350478978225),
    (0.631326076346, 0.334136672344), (0.679073381078, 0.29645404267),
    (0.73597236153, 0.294721285802), (0.782865376271, 0.321305281656),
    (0.740312274764, 0.341849376713), (0.68499850091, 0.343734332172),
    (0.353167761422, 0.746189164237), (0.414587777921, 0.719053835073),
    (0.477677654595, 0.706835892494), (0.522732900812, 0.717092275768),
    (0.569832064287, 0.705414478982), (0.635195811927, 0.71565572516),
    (0.69951672331, 0.739419187253), (0.639447159575, 0.805236879972),
    (0.576410514055, 0.835436670169), (0.525398405766, 0.841706377792),
    (0.47641545769, 0.837505914975), (0.41379548902, 0.810045601727),
    (0.380084785646, 0.749979603086), (0.477955996282, 0.74513234612),
    (0.523389793327, 0.748924302636), (0.571057789237, 0.74332894691),
    (0.672409137852, 0.744177032192), (0.572539621444, 0.776609286626),
    (0.5240106503, 0.783370783245), (0.477561227414, 0.778476346951)])

TPL_MIN, TPL_MAX = np.min(TEMPLATE, axis=0), np.max(TEMPLATE, axis=0)
MINMAX_TEMPLATE = (TEMPLATE - TPL_MIN) / (TPL_MAX - TPL_MIN)
MINMAX_TEMPLATE+=np.array([0,0.15])#important

INNER_EYES_AND_BOTTOM_LIP = [39, 42, 57]
npLandmarkIndices = np.array(INNER_EYES_AND_BOTTOM_LIP)

# dstLandmarks = 256 * MINMAX_TEMPLATE[npLandmarkIndices]
dstLandmarks = 256 * MINMAX_TEMPLATE

FACE_POINTS = list(range(17, 68))
MOUTH_POINTS = list(range(48, 61))
RIGHT_BROW_POINTS = list(range(17, 22))
LEFT_BROW_POINTS = list(range(22, 27))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
NOSE_POINTS = list(range(27, 35))
JAW_POINTS = list(range(0, 17))

# # Points used to line up the images.
# ALIGN_POINTS = LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS + RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS
ALIGN_POINTS=[39,42,57]


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


all_dir = get_dir()
for p in all_dir[0:1]:

    p = p.strip()
    all_image = get_all_image(p)
    filename = p.split("\\")[-2] + p.split("\\")[-1]
    all_bb=np.load("./align_data/bb/"+filename+".npy")
    all_landmark = np.load("./align_data/landmark/" + filename + ".npy")

    new_path=p.split("\\")[-2] +"/"+ p.split("\\")[-1]+"/"

    i=0
    for path in all_image:
        bgr = cv2.imread(path)
        bb=all_bb[i,:]
        npLandmarks = np.float32(all_landmark[i,:,:])

        face=bgr[int(bb[1]):int(bb[3]),int(bb[0]):int(bb[2])]

        H = cv2.estimateRigidTransform(npLandmarks[ALIGN_POINTS], dstLandmarks[ALIGN_POINTS],0)

        align_face=cv2.warpAffine(bgr, H, (256, 256))

        if not os.path.exists("./align_face/"+new_path):
            os.makedirs("./align_face/"+new_path)

        if not os.path.exists("./face/"+new_path):
            os.makedirs("./face/"+new_path)

        cv2.imwrite("./face/"+new_path+path.split("\\")[-1],face)
        cv2.imwrite("./align_face/" + new_path + path.split("\\")[-1], align_face)

        i+=1

    print(p+' done')
