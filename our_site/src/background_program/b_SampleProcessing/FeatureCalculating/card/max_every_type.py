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
        sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,max(abs(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m-%d'),type order by student_num,DATE_FORMAT(date, '%Y-%m-%d')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        student_num=result[0][0]
        flag=0
        max_amount=[0,0,0,0,0,0,0]
        name_tag=['charge','exercise','snack','study','market','canteen','other']
        tag=0
        num=0
        month_tag=0
        year_tag=2200
        first=2
        result[0][1].split('-')
        if int(result[0][1][5:7])<9:
            num=1
            first=1
        for re in result:
            re[1].split('-')
            month=int(re[1][5:7])
            year2=int(re[1][0:4])
            if re[0]!=student_num:
                flag=2
                num=0
                first=2
            elif int(year2)>int(year_tag) and month_tag<9 and flag!=2:
                year=year_tag-1
                student_num2=str(student_num) + (str)(year)
                max_amount=self.SQL_deal(name_tag,max_amount,student_num2)  
                tag=1
                first=2
            elif int(year2)>int(year_tag) and month_tag>=9 and month>=9 and flag!=2:
                year=year_tag
                student_num2=str(student_num) + (str)(year)
                max_amount=self.SQL_deal(name_tag,max_amount,student_num2)  
                tag=1
                first=2
            elif month>=9 and flag!=2:
                if first==1:
                    first=2
                if tag==0 and num!=0 and first==0:
                    year=int(re[1][0:4])-1
                    student_num2=str(student_num) + (str)(year)
                    max_amount=self.SQL_deal(name_tag,max_amount,student_num2) 
                    tag=1
                    first=2
            if re[0]==student_num:
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
            if flag==2:
                if month_tag<9:
                    year=int(year_tag)-1
                else:
                    year=int(year_tag)
                student_num2=str(student_num) + (str)(year)
                max_amount=self.SQL_deal(name_tag,max_amount,student_num2)
                flag=0
                year_tag=int(re[1][0:4])
            month_tag=int(re[1][5:7])
            year_tag=int(re[1][0:4])
            if month<7:
                tag=0
                num=1
                first=0
            student_num=re[0]
    def SQL_deal(self,name_tag,max_amount,student_num):
        for i in range(7):
            name=str(name_tag[i]+'_day_max_amount')
            sql = "update students set {0}={1} where student_num='{2}'"
            self.executer.execute(sql.format(name, float(max_amount[i]),str(student_num)))   
            max_amount[i]=0; 
        return max_amount
if __name__=='__main__':
    import datetime
    m=max_every_type()
    start=datetime.datetime.now()
    m.calculate()
    endtime = datetime.datetime.now()
    print((endtime - start).seconds)
    