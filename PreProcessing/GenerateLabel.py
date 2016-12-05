import numpy as np
import xlrd

# 生成标签
book = xlrd.open_workbook("CASME2-coding-20140508.xlsx")
sheet = book.sheet_by_index(0)
for i in range(1, 256):  # 256
    row = sheet.row_values(i)
    name = "sub" + row[0] + row[1]
    a = np.load("./data/" + name + ".npy")
    label = np.zeros((1, a.shape[0]), dtype=np.int32)
    start = int(row[3])
    end = int(row[5])
    label[0, start - 1:end] = 1
    np.save("./label/" + name + ".npy", label)
