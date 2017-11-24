'''
Created on 2017年11月24日

@author: LI
'''
import matplotlib
import matplotlib.pyplot as plt
from Tools import MyDataBase

db = MyDataBase.MyDataBase("软件学院")
executer = db.getExcuter()
sql = "select score from students where score<> 0;"
executer.execute(sql)
result = executer.fetchall()
result2 = []
# for i in result:
#     print(i)
# #     if i!= 0.0:
# #         print(i)
# #         result2.append(i)

Xaixs = []
for i in range(len(result)):
    Xaixs.append(1+i*0.5)

# plt.plot([1,3,5,7,12])
plt.plot(result,Xaixs)
# plt.axis([0,0,0,100])
plt.show()
db.close

