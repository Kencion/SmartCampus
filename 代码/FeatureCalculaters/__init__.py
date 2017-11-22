# 鐗瑰緛璁＄畻妯″潡
__all__ = ['library', 'scholarship', 'subsidy']

if __name__ == '__main__':
    from Tools import *
    from FeatureCalculaters import FeatureCalculater
    
    class start(FeatureCalculater.FeatureCalculater):
        '''
                璁＄畻鑾峰緱濂栧閲戠殑閲戦
        '''
        def setLevel(self):
            pass
            
        @MyLogger.myException
        def calculate(self):
            sql = "select distinct student_num,student_name,grade,student_type from subsidy"
            self.executer.execute(sql)
            result = self.executer.fetchall()
            # print(result)
            for re in result:
                count = int(re[2])
                if str(re[3]) == '普通高校本科学生':
                    while count <= int(re[2]) + 3 & count <= 2017:
                        sql = "insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                        self.executer.execute(sql, (str(re[0]) + str(count), re[1], str(re[2]), re[3]))
                        count = count + 1
                else:
                    while count <= int(re[2]) + 2 & count <= 2017:
                        sql = "insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                        self.executer.execute(sql, (str(re[0]) + str(count), re[1], str(re[2]), re[3]))
                        count = count + 1
            
        @MyLogger.myException
        def rankit(self):
            pass
    t = start()
    t.calculate()
    t.afterCalculate()
