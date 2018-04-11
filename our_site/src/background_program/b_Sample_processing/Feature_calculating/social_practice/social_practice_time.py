'''
Created on 2018年4月11日

@author: yzh
'''


from background_program.z_Tools.my_exceptions import my_exception_handler
from ..FeatureCalculater import FeatureCalculater


class social_practice_time(FeatureCalculater):

    def __init__(self):
        
        FeatureCalculater.__init__(self, feature_name='social_practice_time')
        
        '''
                        实现将数据库表social_practice中原来无法处理的队员一列分离开来，插入到原来表中。
        '''
        
        sql = "select * from social_practice"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        
        for i in e:
            Serial_num = str(i[0])
            Stu_num = str(i[1])
            Stu_name = str(i[2])
            Stu_type = str(i[3])
            College = str(i[4])
            Grade = str(i[5])
            Department = str(i[6])
            Practice_name = str(i[7])
            Start_time = str(i[8])
            Finish_time = str(i[9])
            Practice_place = str(i[10])
            Keywords = str(i[11])
            Introduction = str(i[12])
            School_key_projects_or_not = str(i[13])
            College_key_projects_or_not = str(i[14])
            Team_members = str(i[15])
            Team_leader_or_not = str(i[16])
            
            for stu in Team_members[:-1].split(')'):
                stu = stu.strip('\n')
                Stu_name = stu.split('(')[0]
                info = stu.split('(')[1]
                Stu_num = info.split(',')[0]
                College = info.split(',')[1]
                Stu_type = info.split(',')[2]
                Team_leader_or_not = '0'
                
                sql = "INSERT IGNORE INTO social_practice (Serial_num, Stu_num,Stu_name,Stu_type,\
College,Grade,Department,Practice_name,Start_time,Finish_time,Practice_place,Keywords,\
Introduction,School_key_projects_or_not,College_key_projects_or_not,Team_members,Team_leader_or_not)\
VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format\
(Serial_num, Stu_num,Stu_name,Stu_type,College,Grade,Department,Practice_name,Start_time,Finish_time,\
Practice_place,Keywords,Introduction,School_key_projects_or_not,College_key_projects_or_not,\
Team_members,Team_leader_or_not)

                self.executer.execute(sql)
                 
    @my_exception_handler
    def calculate(self):
        '''
                计算社会实践实践时间。
                思路：从social_practice表中获取student_num以及学年（根据start_time来划分），实践时间。
                然后根据student_num关键字填入students表中。
        '''
        sql = "select Stu_num,DATE_FORMAT(Start_time,'%Y'),DATE_FORMAT(Start_time,'%c'),\
        unix_timestamp(Finish_time)-unix_timestamp(Start_time) from social_practice"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        
        for i in e:
            stu_num = str(i[0])
            year = int(i[1])
            month = int(i[2])
            
            if(month < 9):
                year = year - 1
                
            time = str(i[3])
            sql = "update students set social_practice_time = '" + str(time) + \
            "' where student_num = '" + str(stu_num) + str(year) + "'"
            self.executer.execute(sql)
            t = self.executer.execute(sql)
            
            if t == 0:
                self.add_student(str(stu_num) + str(year))
                self.executer.execute(sql)
                
            else:
                print("计算社会实践时间这个学生这个学年可能有问题：" + str(stu_num) + "  "+str(year))
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
