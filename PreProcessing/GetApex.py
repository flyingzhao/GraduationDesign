import numpy as np
import xlrd
import os
import cv2

book = xlrd.open_workbook("CASME2-coding-20140508.xlsx")
sheet = book.sheet_by_index(0)

base_dir="F:/CASME2/CASME2_RAW/CASME2-RAW/"

for i in range(1, 256):  # 256
    row = sheet.row_values(i)
    name =base_dir+ "sub" + row[0] +"/"+ row[1]+"/"
    apex_index=int(row[4])
    label=row[8]

    label_dir="./Expression/"+label
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    for j in range(apex_index,apex_index+1):
        img_name=name+"img"+str(j)+".jpg"
        img=cv2.imread(img_name)
        cv2.imwrite(label_dir+"/"+row[0]+row[1]+"img"+str(j)+".jpg",img)

