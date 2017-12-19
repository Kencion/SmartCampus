'''
Created on 2017年11月29日

@author: yzh
'''
from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

class Failed_failed_num(FeatureCalculater):

    @MyLogger.myException
    def calculate(self):
        '''
                            计算failed_failed_num：挂科重修后任然没通过的数目
                            从score表中取出信息，按照score表中的学号索取到students表的学号，再将挂科信息填充到students表中。
        '''
        sql = "select student_num,failed_num,failed_pass_num from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            failed_failed_num = 0
#             print(i)
            if i[1] is not None and i[2] is not None:
                student_num = str(i[0])
                failed_num = int(i[1])
                failed_pass_num = int(i[2])
                failed_failed_num = failed_num - failed_pass_num
                sql = "update students set failed_failed_num = '"+str(failed_failed_num)+"' where student_num = '"+str(student_num)+"'"
#                 print(sql)
                self.executer.execute(sql)
            
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.cluster(self,featureName='failed_failed_num', clusters=4, sql="SELECT failed_failed_num FROM students WHERE failed_failed_num != NULL")
        sql = "SELECT max(failed_failed_num) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "failed_failed_num" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
failed_failed_num1 = Failed_failed_num()
failed_failed_num1.calculate()