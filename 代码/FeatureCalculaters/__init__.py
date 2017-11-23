'''
特征计算模块
每个文件都要和数据库中的字段同名，按表名放
模块名字以1结尾的表示只要跑一次
模块名字以0结尾的表示还没跑
其他的是一次跑一个学生的

#目前已经在统计的属性有：
*这里大家帮忙一起写下
*
这样跑下来大概需要 1h
'''


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
            for re in result:
                count = int(re[2])
                if str(re[3]) == '普通高校本科学生':
                    while count <= int(re[2]) + 8 and count <= 2016:
                        sql = "insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                        self.executer.execute(sql, (str(re[0]) + str(count), re[1], str(re[2]), re[3]))
                        count = count + 1
                        
                    print(count)
                else:
                    while count <= int(re[2]) + 8 and count <= 2016:
                        sql = "insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                        self.executer.execute(sql, (str(re[0]) + str(count), re[1], str(re[2]), re[3]))
                        count = count + 1
            
        @MyLogger.myException
        def rankit(self):
            pass
        
    t = start()
    t.calculate()
    t.afterCalculate()
