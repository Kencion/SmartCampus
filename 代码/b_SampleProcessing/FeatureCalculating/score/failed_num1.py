'''
Created on 2017年11月22日

@author: yzh
'''

from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

class failed_num1(FeatureCalculater):
    
    @MyLogger.myException
    def calculate(self):
        '''
                            计算挂科的数目
                            从score表中取出信息，按照score表中的学号索取到students表的学号，再将挂科信息填充到students表中。
        '''
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
#             print(str(i[0]))
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade,2017):
                failed_num1 = 0
                pass_num1 = 0
                failed_num2 = 0
                pass_num2 = 0
                failed_num = 0
                pass_num = 0
                year1 = str(year)+'/'+str(year+1)+'-1'
                year2 = str(year)+'/'+str(year+1)+'-2'
                sql = "select substring_index(failed_num,'(',1),substring_index(failed_num,'(',-1) from score where stu_num = '"+stu_num+"' and school_year = '"+year1+"'"   
#                 print(sql)
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
#                 print(stu1)
                
                if stu1 is not None :
                    failed_num1 = int(stu1[0])
                    pass_num1 = int(str(stu1[1])[:-1])
                sql = "select substring_index(failed_num,'(',1),substring_index(failed_num,'(',-1) from score where stu_num = '"+stu_num+"' and school_year = '"+year2+"'"   
#                 print(sql)
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
#                 print(stu2)
                if stu2 is not None:
                    failed_num2 = int(stu2[0])
                    pass_num2 = int(str(stu2[1])[:-1])
                    
                failed_num = failed_num1 + failed_num2
                pass_num = pass_num1 + pass_num2
                sql = "update students set failed_num = "+str(failed_num)+" where student_num = '"+stu_num+str(year)+"'"
#                 sql = "update students set failed_pass_num = "+str(pass_num)+" where student_num = '"+stu_num+str(year)+"'"
#                 print(sql)
                self.executer.execute(sql)
            
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.cluster(self,featureName='failed_num', clusters=4, sql="SELECT failed_num FROM students WHERE failed_num != NULL")
        sql = "SELECT max(failed_num) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "failed_num" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()