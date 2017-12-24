'''
@author: yhj
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class library_borrow_times1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_borrow_times')
        
    @my_exception_handler
    def calculate(self):
        '''
                计算图书馆借阅
        '''
        from boto.sdb.db.sequence import double
        sql = "select student_num,DATE_FORMAT(borrow_date, '%Y-%m'),count(*) from library_borrow group by student_num,DATE_FORMAT(borrow_date, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        sql = "update students set library_borrow_times=0"
        self.executer.execute(sql)
        for re in result:
            re[1].split('-')
            if int(re[1][5:7]) < 9:
                sql = "update students set library_borrow_times=library_borrow_times+%s where student_num=%s"
                self.executer.execute(sql, (double(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
            else:
                sql = "update students set library_borrow_times=library_borrow_times+%s where student_num=%s"
                self.executer.execute(sql, (double(re[2]), str(re[0]) + (str)(re[1][0:4])))
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
