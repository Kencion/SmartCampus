'''
特征计算模块
模块名字以1结尾的表示只要跑一次，其他的是一次跑一个学生的
'''

__all__ = ['library', 'scholarship', 'subsidy']


if __name__ == '__main__':
    from Tools import *
    from FeatureCalculaters import FeatureCalculater
    
    class start(FeatureCalculater.FeatureCalculater):
        '''
                        获取主键         
        '''
        def setLevel(self):
            pass
            
        @MyLogger.myException
        def calculate(self):
            sql = "select distinct student_num,student_name,grade,student_type from subsidy"
            self.executer.execute(sql)
            result = self.executer.fetchall()
#             print(result)
            for re in result:
                count = int(re[2])
                if str(re[3]) == '普通高校本科学生':
                    while count <= int(re[2]) + 8 and count <= 2016:
#                         print(re)
                        sql = "insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                        self.executer.execute(sql, (str(re[0]) + str(count), re[1], str(re[2]), re[3]))
                        count = count + 1
                        
                    print(count)
                else:
                    while count <= int(re[2]) + 8 and count <= 2016:
                        # print(re)
                        sql = "insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                        self.executer.execute(sql, (str(re[0]) + str(count), re[1], str(re[2]), re[3]))
                        count = count + 1
            print("over")
            
        @MyLogger.myException
        def rankit(self):
            pass
        
    t = start()
    t.calculate()
    t.afterCalculate()
