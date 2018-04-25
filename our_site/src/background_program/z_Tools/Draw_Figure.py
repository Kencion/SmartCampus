'''
Created on 2018年4月20日

@author: YHJ
'''
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater
import matplotlib as plt
class Draw_Figure(FeatureCalculater):
    def draw_figure(self):
        sql="SELECT count(*) from students_float where scholarship_amount!=0"
        self.executer.execute(sql)
        data1=self.executer.fetchone()
        sql="SELECT count(*) from students_float"
        self.executer.execute(sql)
        data2=self.executer.fetchone()
        data1=int(data1[0])
        data2=int(data2[0])
        
if __name__=='__main__':
    Draw_Figure().draw_figure()