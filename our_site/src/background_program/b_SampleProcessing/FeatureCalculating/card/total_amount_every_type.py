'''
Created on 2017年12月19日

@author: YHJ
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class total_amount_every_type(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算每种消费的总额
        '''
        sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,abs(sum(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m'),type order by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        count=[0,0,0,0,0,0,0]
        student_num=result[0][0]
        flag=0
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
                    count[6]+=int(re[3])
                elif str(re[2])=='canteen':
                    count[5]+=int(re[3])
                elif str(re[2])=='market':
                    count[4]+=int(re[3])
                elif str(re[2])=='study':
                    count[3]+=int(re[3])
                elif str(re[2])=='snack':
                    count[2]+=int(re[3])
                elif str(re[2])=='exercise':
                    count[1]+=int(re[3])
                else: 
                    count[0]+=int(re[3])
            name_tag=['charge','exercise','snack','study','market','canteen','other']
            if flag==1 or flag==2:
                for i in range(7): 
                    name=str(name_tag[i]+'_total_amount')
                    sql = "update students set {0}={1} where student_num='{2}'"
                    self.executer.execute(sql.format(name, float(count[i]),str(student_num) + (str)(year)))
                    count[i]=0
                flag=0
                print('跑成功一次')
            student_num=re[0]
if __name__=='__main__':
    p=total_amount_every_type()
    p.calculate() 
                
            
                
                
                
                
                
                
                
                