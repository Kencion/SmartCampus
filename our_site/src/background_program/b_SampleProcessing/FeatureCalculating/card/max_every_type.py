'''
Created on 2017年12月19日

@author: YHJ
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class max_every_type(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算每种消费的日消费最大额
        '''
        sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,max(abs(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m-%d'),type order by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        student_num=result[0][0]
        flag=0
        max_amount=[0,0,0,0,0,0,0]
        for re in result:
            re[1].split('-')
            month=int(re[1][6:7])
            year=int(re[1][0:4])-1
            if month>=9:
                year=int(re[1][0:4])
                flag=1
            elif str(re[0])!=str(student_num):
                flag=2
            else:
                if str(re[2])=='other':
                    if int(re[3])>max_amount[6]:
                        max_amount[6]=int(re[3])
                elif str(re[2])=='canteen':
                    if int(re[3])>max_amount[5]:
                        max_amount[5]=int(re[3])
                elif str(re[2])=='market':
                    if int(re[3])>max_amount[4]:
                        max_amount[4]=int(re[3])
                elif str(re[2])=='study':
                    if int(re[3])>max_amount[3]:
                        max_amount[3]=int(re[3])
                elif str(re[2])=='snack':
                    if int(re[3])>max_amount[2]:
                        max_amount[2]=int(re[3])
                elif str(re[2])=='exercise':
                    if int(re[3])>max_amount[1]:
                        max_amount[1]=int(re[3])
                else: 
                    if int(re[3])>max_amount[0]:
                        max_amount[0]=int(re[3])
            name_tag=['charge','exercise','snack','study','market','canteen','other']
            if flag==1 or flag==2:
                for i in range(7):
                    name=str(name_tag[i]+'_day_max_amount')
                    sql = "update students set {0}={1} where student_num='{2}'"
                    self.executer.execute(sql.format(name, float(max_amount[i]),str(student_num) + (str)(year)))   
                    max_amount[i]=0; 
                print("跑了一次")
                flag=0
            student_num=re[0]
if __name__=='__main__':
    m=max_every_type()
    m.calculate()
    