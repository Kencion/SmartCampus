'''
Created on 2017年11月23日

@author: jack
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class hornorary_rank(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算一学年内获得荣誉的等级
    # 一个学生可能会获得很多的荣誉称号
    # 这里先直接搜索到一条就当成是这个
    #
    # 之后会用数值代表这个，比如一个学生获得一次校级（5），一次院级（3），那就5+3=8
        '''
        sql = "update students set hornorary_rank=0"
        self.executer.execute(sql)
        sql = "select student_num,left(grant_year,4),grant_rank from hornorary_handled"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            hornorary_rank = 0
            if re[2] == '校级':
                hornorary_rank += 5
            elif re[2] == '院级':
                hornorary_rank += 3
            sql = "update students set hornorary_rank=hornorary_rank+%s where student_num=%s"
            self.executer.execute(sql, (int(hornorary_rank), (re[0] + re[1])))
            
#     @MyLogger.myException
#     def cluster(self):
#         sql="SELECT max(hornorary_rank) FROM students"
#         self.executer.execute(sql)
#         result=self.executer.fetchone()[0]
#         max_num=int(result)
#         maxx,minn,cent=FeatureCalculater.cluster(self,featureName='hornorary_rank', clusters=4, sql="SELECT hornorary_rank FROM students WHERE hornorary_rank != 0")
#         maxx[len(maxx) - 1] = max_num
#         
#         with open(r"Cluster_Feature", "a", encoding='utf8') as f:
#             f.write( "hornorary_rank字段" + '\n')
#             f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
#             print("write.....")
#             for i in range(len(cent)):
#                 f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
#             f.close()    
