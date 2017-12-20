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
        sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,abs(sum(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m'),type order by student_num,DATE_FORMAT(date, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        count=[0,0,0,0,0,0,0]
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
                    #print(str(student_num) + (str)(year)+"——————————————"+str(count[4]))
                    for i in range(7): 
                        name=str(name_tag[i]+'_total_amount')
                        sql = "update students set {0}={1} where student_num='{2}'"
                        self.executer.execute(sql.format(name, float(count[i]),str(student_num) + (str)(year)))
                        count[i]=0
                    count_num+=1
                    tag=1
                    first=2
            if re[0]==student_num:
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
            if flag==2:
                if month_tag<9:
                    year=int(year_tag)-1
                else:
                    year=int(year_tag)
                #print(str(student_num) + (str)(year)+"——————————————"+str(count[4]))
                for i in range(7): 
                    name=str(name_tag[i]+'_total_amount')
                    sql = "update students set {0}={1} where student_num='{2}'"
                    self.executer.execute(sql.format(name, float(count[i]),str(student_num) + (str)(year)))
                    count[i]=0
                count_num+=1
                flag=0
            month_tag=int(re[1][6:7])
            year_tag=int(re[1][0:4])
            if month<9 and first==2:
                tag=0
                num=1
                first=0
            student_num=re[0]
        print(str(count_num)+"*************")
if __name__=='__main__':
    import datetime
    p=total_amount_every_type()
    #print("helo:"+str(n)+"-----")
    start=datetime.datetime.now()
    p.calculate() 
    endtime = datetime.datetime.now()
    print((endtime - start).seconds)
            
                
                
                
                
                
                
                
                