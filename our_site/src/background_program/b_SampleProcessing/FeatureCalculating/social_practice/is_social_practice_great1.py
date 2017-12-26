'''
Created on 2017年11月23日

@author: yzh
'''


from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class is_social_practice_great1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='is_social_practice_great')
    
    @my_exception_handler
    def calculate(self):
        '''
                判断是否是院级或者校级重点。
                思路：从social_practice表中获取student_num以及学年（根据start_time来划分），是否是重点，然后根据student_num关键字填入students表中。
        '''
        sql = "select stu_num,DATE_FORMAT(start_time,'%Y'),DATE_FORMAT(start_time,'%c'),School_key_projects_or_not,College_key_projects_or_not from social_practice"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            year = int(i[1])
            month = int(i[2])
            if(month < 9):
                year = year - 1
            School_key_projects_or_not = i[3]
            College_key_projects_or_not = i[4]
            if(School_key_projects_or_not == "否" and College_key_projects_or_not == "否"):
                is_social_practice_great = 0
            else:
                is_social_practice_great = 1
            sql = "update students set is_social_practice_great = '" + str(is_social_practice_great) + "' where student_num = '" + str(stu_num) + str(year) + "'"
            self.executer.execute(sql)
            t = self.executer.execute(sql)
            if t == 0:
                self.add_student(str(stu_num) + str(year))
                self.executer.execute(sql)
            else:
                print("计算是否是院级或者校级重点这个学生这个学年可能有问题：" + str(stu_num) + "  "+str(year))
   
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
