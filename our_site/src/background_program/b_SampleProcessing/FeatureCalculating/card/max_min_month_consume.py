'''
Created on 2017年12月19日

@author: YHJ
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class max_min_month_consume(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算月消费最大值和最小值
        '''
        sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,sum(abs(transaction_amount)),sum(abs(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m'),type order by student_num,DATE_FORMAT(date, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        max_count=[0,0,0,0,0,0,0]
        min_count=[500000,500000,500000,500000,500000,500000,500000]
        student_num=result[0][0]
        count_num=0
        flag=0
        name_tag=['charge','exercise','snack','study','market','canteen','other']
        tag=0
        num=0
        month_tag=0
        year_tag=0
        first=2
        result[0][1].split('-')
        if int(result[0][1][6:7])<9:
            num=1
            first=1
        for re in result:
            re[1].split('-')
            month=int(re[1][6:7])
            year=int(re[1][0:4])-1
            if re[0]!=student_num:
                flag=2
                num=0
                first=2
            elif month>=9:
                if first==1:
                    first=2
                if tag==0 and num!=0 and first==0:
                    year=int(re[1][0:4])-1
                    for i in range(7): 
                        name=str(name_tag[i]+'_max_amount')
                        sql = "update students set {0}={1} where student_num='{2}'"
                        self.executer.execute(sql.format(name, float(max_count[i]),str(student_num) + (str)(year)))
                        max_count[i]=0
                        if int(min_count[i])==500000:
                            min_count[i]=0
                        name2=str(name_tag[i]+'_min_amount')
                        sql = "update students set {0}={1} where student_num='{2}'"
                        self.executer.execute(sql.format(name2, float(min_count[i]),str(student_num) + (str)(year)))
                        min_count[i]=500000
                    count_num+=1
                    tag=1
                    first=2
            if re[0]==student_num:
                if str(re[2])=='other':
                    if int(re[3])>max_count[6]:
                        max_count[6]=int(re[3])
                    if int(re[4])<min_count[6]:
                        min_count[6]=int(re[4])
                elif str(re[2])=='canteen':
                    if int(re[3])>max_count[5]:
                        max_count[5]=int(re[3])
                    if int(re[4])<min_count[5]:
                        min_count[5]=int(re[4])
                elif str(re[2])=='market':
                    if int(re[3])>max_count[4]:
                        max_count[4]=int(re[3])
                    if int(re[4])<min_count[4]:
                        min_count[4]=int(re[4])
                elif str(re[2])=='study':
                    if int(re[3])>max_count[3]:
                        max_count[3]=int(re[3])
                    if int(re[4])<min_count[3]:
                        min_count[3]=int(re[4])
                elif str(re[2])=='snack':
                    if int(re[3])>max_count[2]:
                        max_count[2]=int(re[3])
                    if int(re[4])<min_count[2]:
                        min_count[2]=int(re[4])
                elif str(re[2])=='exercise':
                    if int(re[3])>max_count[1]:
                        max_count[1]=int(re[3])
                    if int(re[4])<min_count[1]:
                        min_count[1]=int(re[4])
                else: 
                    if int(re[3])>max_count[0]:
                        max_count[0]=int(re[3])
                    if int(re[4])<min_count[0]:
                        min_count[0]=int(re[4])
            if flag==2:
                if month_tag<9:
                    year=int(year_tag)-1
                else:
                    year=int(year_tag)
                for i in range(7): 
                    name=str(name_tag[i]+'_max_amount')
                    sql = "update students set {0}={1} where student_num='{2}'"
                    self.executer.execute(sql.format(name, float(max_count[i]),str(student_num) + (str)(year)))
                    max_count[i]=0
                    if int(min_count[i])==500000:
                        min_count[i]=0
                    name2=str(name_tag[i]+'_min_amount')
                    sql = "update students set {0}={1} where student_num='{2}'"
                    self.executer.execute(sql.format(name2, float(min_count[i]),str(student_num) + (str)(year)))
                    min_count[i]=500000
                count_num+=1
                flag=0
            month_tag=int(re[1][6:7])
            year_tag=int(re[1][0:4])
            if month<9 and first==2:
                tag=0
                num=1
                first=0
            student_num=re[0]
if __name__=='__main__':
    import datetime
    p=max_min_month_consume()
    start=datetime.datetime.now()
    p.calculate() 
    endtime = datetime.datetime.now()
    print((endtime - start).seconds)
            
                
                
                
                
                
                
                
                