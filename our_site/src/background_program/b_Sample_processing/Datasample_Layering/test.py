#import b_DatasampleLayering.Random_Data as rd
import pymysql.cursors
import time
from datetime import date, datetime
#from a_DataProssing.Datasample_layering.Random_Data import  Random_Data

class test():
    def calcute(self):
        train_data=[]
        test_data=[]
        conn=pymysql.connect(
                        host='172.16.20.5',
                        user='root',
                        password='',
                        db='软件学院',
                        charset='utf8mb4'
                        )
        try:
             with conn.cursor() as cursor:
                 #从数据库提取特征属性
                sql="select subsidy_amount,scholarship_amount from students where subsidy_amount!=0 and scholarship_amount!=0"
                cursor.execute(sql)
                result=cursor.fetchall()
                #从数据库获取分类标签
                sql="select distinct(scholarship_amount) from students"
                cursor.execute(sql)
                label=cursor.fetchall()
#                 print(result)
#                 print(label)
                #获取训练集和验证集
                from background_program.b_Sample_processing.Datasample_Layering import Random_Data
                train_data,test_data=Random_Data.Random_Data.group(self, result, label, 0.1)
                
                return train_data,test_data
        finally:
            conn.close()
if __name__=='__main__':
    te=test()
    te.calcute()
