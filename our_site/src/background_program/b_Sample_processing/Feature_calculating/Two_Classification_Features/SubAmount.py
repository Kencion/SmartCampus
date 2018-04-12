'''
Created on 2018年4月12日

@author: YHJ
'''
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater
class SubAmount(FeatureCalculater):
    """
        将student_float表中的subdisy_amount二分类进student_int表
    0表示未获得助学金，1表示获得助学金
    """
    def Classifier(self):
        sql = "SELECT student_num,sum(subsidy_amount) FROM students_float  group by student_num"
        self.executer.execute(sql)
        result=self.executer.fetchall()
        for re in result:
            if int(re[1])!=0:
                re[1]=1
            else:
                re[1]=0
            sql = "update students_int set subsidy_amount = {0} where student_num = {1}".format(float(re[1]),str(re[0])) 
            n_update = self.executer.execute(sql)
            if n_update == 0:
                try:
                    sql = 'insert into students_int(student_num) values({0})'.format(str(re[0]))
                    self.executer.execute(sql)
                except:
                    pass
                sql = "update students_int set  subsidy_amount= {0} where student_num = {1}".format(float(re[1]),str(re[0])) 
                self.executer.execute(sql)
if __name__=="__main__":
    sa=SubAmount()
    sa.Classifier()