'''
Created on 2017年11月22日

@author: yzh

some error
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class social_practice1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='social_practice')
    
    @my_exception_handler
    def calculate(self):
        '''
        实现将数据库表social_practice中原来无法处理的队员一列分离开来，插入到原来表中。
         判断是否是院级或者校级重点。
            思路：从social_practice表中获取student_num以及学年（根据start_time来划分），是否是重点，然后根据stu_num关键字填入students表中。
        '''
        sql = "select stu_num,DATE_FORMAT(start_time,'%Y'),DATE_FORMAT(start_time,'%c'),School_key_projects_or_not,College_key_projects_or_not from social_practice"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            year = int(i[1])
            month = int(i[2])
            # print("month = "+str(month))
            if(month < 9):
                year = year - 1
            School_key_projects_or_not = i[3]
            College_key_projects_or_not = i[4]
            if(School_key_projects_or_not == "否" and College_key_projects_or_not == "否"):
                is_social_practice_great = 0
            else:
                is_social_practice_great = 1
            sql = "update students set social_practice = '" + str(is_social_practice_great) + "' where student_num = '" + str(stu_num) + str(year) + "'"
            # print(sql)
            self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
