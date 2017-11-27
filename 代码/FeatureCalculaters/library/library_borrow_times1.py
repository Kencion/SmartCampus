'''
@author: yhj
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class library_borrow_times1(FeatureCalculater.FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算图书馆借阅
        '''
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
    def cluster(self):
        maxx, minn, cent = FeatureCalculater.FeatureCalculater.cluster(self, featureName='library_borrow_times', clusters=4, sql="SELECT library_borrow_times FROM students WHERE library_borrow_times != 0")
        sql = "SELECT max(library_borrow_times) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"聚类对应的字段区间", "a", encoding='utf8') as f:
            f.write("library_borrow_times" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
