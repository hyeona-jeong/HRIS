import openpyxl
import sys
import os
import pymysql

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

wb = openpyxl.Workbook()

conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
            )
cur = conn.cursor()
query = "SELECT DEPT_BIZ, DEPT_GROUP, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL FROM MAIN_TABLE"
cur.execute(query)
result = cur.fetchall()
w1 = wb["Sheet"]
for i in range(len(result)):
    for j in range(len(result[i])):
        w1.cell(i+1,j+1).value = result[i][j]

new_filename = resource_path('info.xlsx')
wb.save(new_filename)



