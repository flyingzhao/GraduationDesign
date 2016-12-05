import os

"""
    生成所有的目录
"""


def gci(filepath):


    """
    遍历filepath下所有文件，包括子目录
    """
    files = os.listdir(filepath)

    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            if fi_d[-5] is not "s":
                print(os.path.join(filepath, fi_d))
            gci(fi_d)
        else:
            pass

if __name__ == "__main__":
     gci("F:\CASME2\CASME2_RAW\CASME2-RAW")
