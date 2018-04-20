'''
Created on 2018年4月19日

@author: YHJ
'''
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater
from background_program.b_Sample_processing.PreProcessing import Features_Analyse
class Exchange_Data(FeatureCalculater):
    def Add_Datas(self):
        Feature_names=Features_Analyse.fea_names
        sql="select * from students_int limit 10"
        self.executer.execute(sql)
        result=self.executer.fetchall()
        for i in range(len(Feature_names)):
            if i==0:
                for re in result:
                    sql="insert into Analyse_int({0}) values({1})"
                    self.executer.execute(sql.format(Feature_names[i], str(re[i])))
            else:
                for re in result:
                    value=str(Feature_names[i]+"_"+str(re[i]))
                    sql="update Analyse_int set {0}='{1}' where student_num={2}"
                    self.executer.execute(sql.format(Feature_names[i], str(value),re[0]))
if __name__=='__main__':
    Exchange_Data().Add_Datas()
