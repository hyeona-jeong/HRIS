import matplotlib.pyplot as plt
import numpy as np
import pymysql

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

conn = pymysql.connect(
host='192.168.2.20',
user='dev',
password='nori1234',
db='dev',
port=3306,
charset='utf8'
)
cur = conn.cursor()

query = "SELECT COUNT(GENDER) FROM MAIN_TABLE GROUP BY GENDER"
cur.execute(query)
result = cur.fetchall()
male = result[0][0]
female = result[1][0]
total = male + female
ratio = [male/total, female/total]
labels = ['남성', '여성']

plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=90)
plt.show()

query = "SELECT EMP_RANK, COUNT(EMP_RANK) FROM MAIN_TABLE GROUP BY EMP_RANK"
cur.execute(query)
result = cur.fetchall()
rankNum = {
    '사원' : 0, 
    '주임' : 0, 
    '대리' : 0, 
    '과장' : 0, 
    '차장' : 0, 
    '부장' : 0, 
    '이사' : 0, 
    '상무' : 0, 
    '전무' : 0
}   
for rank in result :
    if rank[0] == '사원' :
        rankNum[rank[0]] = (rank[1])
    elif rank[0] == '주임' :
        rankNum[rank[0]] = (rank[1])  
    elif rank[0] == '대리' :
        rankNum[rank[0]] = (rank[1])  
    elif rank[0] == '과장' :
        rankNum[rank[0]] = (rank[1])   
    elif rank[0] == '차장' :
        rankNum[rank[0]] = (rank[1])   
    elif rank[0] == '부장' :
        rankNum[rank[0]] = (rank[1])   
    elif rank[0] == '이사' :
        rankNum[rank[0]] = (rank[1])   
    elif rank[0] == '상무' :
        rankNum[rank[0]] = (rank[1])   
    elif rank[0] == '전무' :
        rankNum[rank[0]] = (rank[1])      

x = np.arange(9)
years = list(rankNum.keys())
values = list(rankNum.values())

plt.bar(x, values)
plt.xticks(x, years)

plt.show()