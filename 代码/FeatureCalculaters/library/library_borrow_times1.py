'''
@author: yhj
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class library_borrow_times1(FeatureCalculater.FeatureCalculater):
    '''
            计算图书馆借阅
    '''
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        from boto.sdb.db.sequence import double
        sql = "select student_num,DATE_FORMAT(borrow_date, '%Y-%m'),count(*) from library_borrow group by student_num,DATE_FORMAT(borrow_date, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        print(result)
        sql = "update students set library_borrow_times=0"
        self.executer.execute(sql)
        for re in result:
            re[1].split('-')
            if int(re[1][5:7]) < 9:
                sql = "update students set library_borrow_times=%s where student_num=%s"
                self.executer.execute(sql, (double(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                # print((str)(int(re[1][0:4])-1)+'/'+((str)(re[1][0:4])))
            else:
                sql = "update students set library_borrow_times=%s where student_num=%s"
                self.executer.execute(sql, (double(re[2]), str(re[0]) + (str)(re[1][0:4])))
                # print((str)(re[1][0:4])+'/'+((str)((int)(re[1][0:4])+1)))
         
            # sql="update students set borrow_times=%s where student_num=%s and school_year=%s"
            # cursor.execute(sql,(int(re[2]),re[0],re[1]))
        
    @MyLogger.myException
    def rankit(self):
        pass
