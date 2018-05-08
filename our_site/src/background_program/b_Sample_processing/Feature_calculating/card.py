from background_program.z_Tools.my_exceptions import my_exception_handler
from .FeatureCalculater import FeatureCalculater
import numpy as np


class canteen_consumption_divide_by_consumption(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='canteen_amount_divide_by_consumption')

    @my_exception_handler
    def calculate(self):
        '''
                            计算食堂消费额占总消费额的比例
        '''
        sql = "select student_num,canteen_total_amount,consumption from students"
        
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
             
            stu_num = i[0]
            
            if i[1] is not None :
                
                canteen_consumption = i[1]
                
                if i[2] is not None:
                    if i[2] != 0:
                        consumption = i[2]
                        res = float(canteen_consumption) / float(consumption)
                    
                        sql = "update students set canteen_amount_divide_by_consumption = " + str(res) + " where student_num = '" + str(stu_num) + "'"
                        self.executer.execute(sql)
                    else:
                        print("总消费额为0，学号是：" + stu_num)
                
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class canteen_times(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='canteen_times')
     
    @my_exception_handler
    def calculate(self):
        '''
                            计算食堂消费次数
        '''
        sql = 'select max(date) from card'
        self.executer.execute(sql)
        lastestItem_date = self.executer.fetchone()[0]
        if lastestItem_date.month < 9:
            lyear = lastestItem_date.year - 1
        else:
            lyear = lastestItem_date.year
        sql = "select distinct(student_num) from card"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            grade = int(stu_num[3:7])
            
            '''
                                    先处理第一年的特殊情况
            '''
            year1 = grade
            year2 = year1 + 1
            sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-07-01' and '" + str(year2) + "-08-31' and type = 'canteen'" 
            self.executer.execute(sql)
            count = self.executer.fetchone()[0]
            if count != 0:
                sql = "update students set canteen_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
                t = self.executer.execute(sql)
                if t == 0:
                    self.add_student(stu_num + str(year1))
                    self.executer.execute(sql)
#                   print(sql)
            else:
                    print("计算食堂消费次数这个学生这个学年可能有问题：" + stu_num + "  " + str(year1))
                    
            for year1 in range(grade + 1, lyear + 1):
                year2 = year1 + 1
                sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '" + str(year2) + "-08-31' and type = 'canteen'" 
                self.executer.execute(sql)
                count = self.executer.fetchone()[0]
                if count != 0:
                    sql = "update students set canteen_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
                    t = self.executer.execute(sql)

                    if t == 0:
                        self.add_student(stu_num + str(year1))
                        self.executer.execute(sql)
#                         print(sql)
                else:
                    print("计算食堂消费次数这个学生这个学年可能有问题：" + stu_num + "  " + str(year1))
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

        
class Consumption(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='Consumption')

    @my_exception_handler
    def calculate(self):
        '''
                            计算总消费额
        '''
        
        sql = 'select max(date) from card'
        self.executer.execute(sql)
        lastestItem_date = self.executer.fetchone()[0]
        if lastestItem_date.month < 9:
            lyear = lastestItem_date.year - 1
        else:
            lyear = lastestItem_date.year
        
        sql = "select distinct(student_num) from card"
        self.executer.execute(sql)
        e = self.executer.fetchall()   
        
        for i in e:
            stu_num = str(i[0])
            grade = int(stu_num[3:7])
            
            '''
                                    先处理第一年的特殊情况
            '''
            year1 = grade
            year2 = year1 + 1
            sql = "select sum(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-07-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 
            self.executer.execute(sql)
            try:
                count = -1 * self.executer.fetchone()[0]
                if count is not None:
                    sql = "update students set Consumption = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
                    t = self.executer.execute(sql)
                    if t == 0:
                        self.add_student(stu_num + str(year1))
                        self.executer.execute(sql)
    #                         print(sql)
                else:
                    print("计算总消费额这个学生这个学年有问题：" + stu_num + "  " + str(year1))
                        
                for year1 in range(grade + 1, lyear + 1):
                    year2 = year1 + 1
                    sql = "select sum(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 
                    self.executer.execute(sql)
                    count = -1 * self.executer.fetchone()[0]
                    if count is not None:
                        sql = "update students set Consumption = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
                        t = self.executer.execute(sql)
                        if t == 0:
                            self.add_student(stu_num + str(year1))
                            self.executer.execute(sql)
    #                         print(sql)
                    else:
                        print("计算总消费额这个学生这个学年有问题：" + stu_num + "  " + str(year1))
            except:
                pass
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class max_every_type(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self)

    @my_exception_handler
    def calculate(self):
        '''
                计算每种消费的日消费最大额
        '''
        sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,max(abs(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m-%d'),type order by student_num,DATE_FORMAT(date, '%Y-%m-%d')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        student_num = result[0][0]
        flag = 0
        max_amount = [0, 0, 0, 0, 0, 0, 0]
        name_tag = ['charge', 'exercise', 'snack', 'study', 'market', 'canteen', 'other']
        tag = 0
        num = 0
        month_tag = 0
        year_tag = 2200
        first = 2
        result[0][1].split('-')
        if int(result[0][1][5:7]) < 9:
            num = 1
            first = 1
        for re in result:
            re[1].split('-')
            month = int(re[1][5:7])
            year2 = int(re[1][0:4])
            if re[0] != student_num:
                flag = 2
                num = 0
                first = 2
            elif int(year2) > int(year_tag) and month_tag < 9 and flag != 2:
                year = year_tag - 1
                student_num2 = str(student_num) + (str)(year)
                max_amount = self.SQL_deal(name_tag, max_amount, student_num2)  
                tag = 1
                first = 2
            elif int(year2) > int(year_tag) and month_tag >= 9 and month >= 9 and flag != 2:
                year = year_tag
                student_num2 = str(student_num) + (str)(year)
                max_amount = self.SQL_deal(name_tag, max_amount, student_num2)  
                tag = 1
                first = 2
            elif month >= 9 and flag != 2:
                if first == 1:
                    first = 2
                if tag == 0 and num != 0 and first == 0:
                    year = int(re[1][0:4]) - 1
                    student_num2 = str(student_num) + (str)(year)
                    max_amount = self.SQL_deal(name_tag, max_amount, student_num2) 
                    tag = 1
                    first = 2
            if re[0] == student_num:
                if str(re[2]) == 'other':
                    if int(re[3]) > max_amount[6]:
                        max_amount[6] = int(re[3])
                elif str(re[2]) == 'canteen':
                    if int(re[3]) > max_amount[5]:
                        max_amount[5] = int(re[3])
                elif str(re[2]) == 'market':
                    if int(re[3]) > max_amount[4]:
                        max_amount[4] = int(re[3])
                elif str(re[2]) == 'study':
                    if int(re[3]) > max_amount[3]:
                        max_amount[3] = int(re[3])
                elif str(re[2]) == 'snack':
                    if int(re[3]) > max_amount[2]:
                        max_amount[2] = int(re[3])
                elif str(re[2]) == 'exercise':
                    if int(re[3]) > max_amount[1]:
                        max_amount[1] = int(re[3])
                else: 
                    if int(re[3]) > max_amount[0]:
                        max_amount[0] = int(re[3])
            if flag == 2:
                if month_tag < 9:
                    year = int(year_tag) - 1
                else:
                    year = int(year_tag)
                student_num2 = str(student_num) + (str)(year)
                max_amount = self.SQL_deal(name_tag, max_amount, student_num2)
                flag = 0
                year_tag = int(re[1][0:4])
            month_tag = int(re[1][5:7])
            year_tag = int(re[1][0:4])
            if month < 7:
                tag = 0
                num = 1
                first = 0
            student_num = re[0]

    def SQL_deal(self, name_tag, max_amount, student_num):
        if student_num is None:
            pass
        else:
            for i in range(7):
                name = str(name_tag[i] + '_day_max_amount')
                sql = "update students set {0}={1} where student_num='{2}'"
                num = self.executer.execute(sql.format(name, float(max_amount[i]), str(student_num)))   
                if num == 0:
                    self.add_student(student_num)
                    self.executer.execute(sql.format(name, float(max_amount[i]), str(student_num)))   
                max_amount[i] = 0; 
        return max_amount

    def cluster(self):
        name_tag = ['charge', 'exercise', 'snack', 'study', 'market', 'canteen', 'other']
        for i in range(7):
            feature_name = str(name_tag[i] + '_day_max_amount')
            self.feature_name = feature_name
            FeatureCalculater.cluster(self, clusters=4)


class max_min_month_consume(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self) 

    @my_exception_handler
    def calculate(self):
        '''
                计算月消费最大值和最小值
        '''
        sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,sum(abs(transaction_amount)),sum(abs(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m'),type order by student_num,DATE_FORMAT(date, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        max_count = [0, 0, 0, 0, 0, 0, 0]
        min_count = [500000, 500000, 500000, 500000, 500000, 500000, 500000]
        student_num = result[0][0]
        count_num = 0
        flag = 0
        name_tag = ['charge', 'exercise', 'snack', 'study', 'market', 'canteen', 'other']
        tag = 0
        num = 0
        month_tag = 0
        year_tag = 2200
        first = 2
        result[0][1].split('-')
        if int(result[0][1][5:7]) < 9:
            num = 1
            first = 1
        for re in result:
            re[1].split('-')
            month = int(re[1][5:7])
            year2 = int(re[1][0:4])
            if re[0] != student_num:
                flag = 2
                num = 0
                first = 2
            elif int(year2) > int(year_tag) and month_tag < 9 and flag != 2:
                year = year_tag - 1
                student_num2 = str(student_num) + (str)(year)
                max_count = self.SQL_deal_max(name_tag, max_count, student_num2)
                min_count = self.SQL_deal_min(name_tag, min_count, student_num2)
                tag = 1
                first = 2
            elif int(year2) > int(year_tag) and month_tag >= 9 and month >= 9 and flag != 2:
                year = year_tag
                student_num2 = str(student_num) + (str)(year)
                max_count = self.SQL_deal_max(name_tag, max_count, student_num2)
                min_count = self.SQL_deal_min(name_tag, min_count, student_num2)
                tag = 1
                first = 2
            elif month >= 9 and flag != 2:
                if first == 1:
                    first = 2
                if tag == 0 and num != 0 and first == 0:
                    year = int(re[1][0:4]) - 1
                    student_num2 = str(student_num) + (str)(year)
                    max_count = self.SQL_deal_max(name_tag, max_count, student_num2)
                    min_count = self.SQL_deal_min(name_tag, min_count, student_num2)
                    tag = 1
                    first = 2
            if re[0] == student_num:
                if str(re[2]) == 'other':
                    if int(re[3]) > max_count[6]:
                        max_count[6] = int(re[3])
                    if int(re[4]) < min_count[6]:
                        min_count[6] = int(re[4])
                elif str(re[2]) == 'canteen':
                    if int(re[3]) > max_count[5]:
                        max_count[5] = int(re[3])
                    if int(re[4]) < min_count[5]:
                        min_count[5] = int(re[4])
                elif str(re[2]) == 'market':
                    if int(re[3]) > max_count[4]:
                        max_count[4] = int(re[3])
                    if int(re[4]) < min_count[4]:
                        min_count[4] = int(re[4])
                elif str(re[2]) == 'study':
                    if int(re[3]) > max_count[3]:
                        max_count[3] = int(re[3])
                    if int(re[4]) < min_count[3]:
                        min_count[3] = int(re[4])
                elif str(re[2]) == 'snack':
                    if int(re[3]) > max_count[2]:
                        max_count[2] = int(re[3])
                    if int(re[4]) < min_count[2]:
                        min_count[2] = int(re[4])
                elif str(re[2]) == 'exercise':
                    if int(re[3]) > max_count[1]:
                        max_count[1] = int(re[3])
                    if int(re[4]) < min_count[1]:
                        min_count[1] = int(re[4])
                else: 
                    if int(re[3]) > max_count[0]:
                        max_count[0] = int(re[3])
                    if int(re[4]) < min_count[0]:
                        min_count[0] = int(re[4])
            if flag == 2:
                if month_tag < 9:
                    year = int(year_tag) - 1
                else:
                    year = int(year_tag)
                student_num2 = str(student_num) + (str)(year)
                max_count = self.SQL_deal_max(name_tag, max_count, student_num2)
                min_count = self.SQL_deal_min(name_tag, min_count, student_num2)
                year_tag = int(re[1][0:4])
                flag = 0
            if re[0] == student_num:
                month_tag = int(re[1][5:7])
                year_tag = int(re[1][0:4])
            if month < 7 and first == 2:
                tag = 0
                num = 1
                first = 0
            student_num = re[0]
#         print("总共插了多少次数据" + str(count_num))

    def SQL_deal_max(self, name_tag, max_count, student_num):
        if student_num is None:
            pass
        else:
            for i in range(7): 
                name = str(name_tag[i] + '_max_amount')
                sql = "update students set {0}={1} where student_num='{2}'"
                num = self.executer.execute(sql.format(name, float(max_count[i]), str(student_num)))
                if num == 0:
                    self.add_student(student_num)
                    self.executer.execute(sql.format(name, float(max_count[i]), str(student_num)))     
                max_count[i] = 0
        return max_count

    def SQL_deal_min(self, name_tag, min_count, student_num):
        if student_num is None:
            pass
        else:
            for i in range(7): 
                if int(min_count[i]) == 500000:
                    min_count[i] = 0
                name2 = str(name_tag[i] + '_min_amount')
                sql = "update students set {0}={1} where student_num='{2}'"
                num = self.executer.execute(sql.format(name2, float(min_count[i]), str(student_num)))
                if num == 0:
                    self.add_student(student_num)
                    self.executer.execute(sql.format(name2, float(min_count[i]), str(student_num)))     
                min_count[i] = 500000
        return min_count

    def cluster(self):
        name_tag = ['charge', 'exercise', 'snack', 'study', 'market', 'canteen', 'other']
        for i in range(7):
            feature_name = str(name_tag[i] + '_min_amount')
            self.feature_name = feature_name
            FeatureCalculater.cluster(self, clusters=4)
        for i in range(7):
            feature_name = str(name_tag[i] + '_max_amount')
            self.feature_name = feature_name
            FeatureCalculater.cluster(self, clusters=4)
                

class mean_median_var(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self)

    def calculate(self):
        
        '''
                获取最早时间、最晚时间
        '''
        sql = 'select min(date),max(date) from card'
        self.executer.execute(sql)
        result = self.executer.fetchone()
        earliestItem_date = result[0]
        lastestItem_date = result[1]  
        '''
                获得 'card' 表中包含的学年
                eg: 2014-06-04应该属于2013-2014学年
                    2015-09-03应该属于2015-2016学年
        '''
        school_year = []
        eyear = int(earliestItem_date.year)
        if earliestItem_date.month < 9 :
            eyear = eyear - 1
            
        lyear = lastestItem_date.year
        if lastestItem_date.month < 9 :
            lyear = lyear - 1
        
        while eyear <= lyear :
            school_year.extend([eyear])
            eyear = eyear + 1  
        
#         print()
#         print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '获得student_num_list......')
        '''
                获得 'card' 表中包含的student_num的集合
                存放在student_num_list中
        '''    
        sql = 'select distinct student_num from card ' 
        self.executer.execute(sql)
        student_num_list = self.executer.fetchall()
        '''
                获得所有的消费类型
                存放在type_list中
        '''
        sql = 'select distinct type from card' 
        self.executer.execute(sql)
        type_list = self.executer.fetchall()
        
        for student_num in student_num_list:
       
            grade = int(student_num[0][3:7])
          
            for one_type in type_list:
                for year in school_year:
                    if int(year) < grade:
                        continue 
                    sql = 'select abs(transaction_amount) from card where student_num = "'"{0}"'" and ((year(date)={1} and month(date)>8) or (year(date)={2} and month(date)<9)) and type="'"{3}"'"'
                    self.executer.execute(sql.format(student_num[0], int(year), int(year) + 1, one_type[0]))
                    result = list(self.executer.fetchall())
                    
                    if int(year) == grade :
                        sql = 'select abs(transaction_amount) from card where student_num = "'"{0}"'" and year(date)={1} and month(date)<9 and type="'"{2}"'"'
                        self.executer.execute(sql.format(student_num[0], int(year), one_type[0]))
                        result.extend(list(self.executer.fetchall()))
                    
                    if len(result) > 0:
                        mean, median, var = self.get_result(result)
                        mean, median, var = round(mean, 3), round(median, 3), round(var, 3)
                        sql = 'update students set {1}={2},{3}={4},{5}={6} where student_num ="'"{0}"'"'
                        affectedRows = self.executer.execute(sql.format(str(student_num[0]) + str(year), "mean_of_" + str(one_type[0]), mean, "median_of_" + str(one_type[0]), median, "var_of_" + str(one_type[0]), var))
#                         if affectedRows == 0 :
#                             self.add_student(str(student_num[0]) + str(year))
#                             self.executer.execute(sql)

    '''
        计算并返回输入参数 'datalist' 的平均值、中位数、方差 
    @param :
        datalist: 1d_array-like ，shape(n_items) ,the original data  
    @return : 
        result(list): [平均值、中位数、方差]
    '''

    def get_result(self, datalist):
        mean = np.mean(datalist)
        median = np.median(datalist)
        var = np.var(datalist)
        
        return mean, median, var
    
    def cluster(self):
        name_tag = ['charge', 'exercise', 'snack', 'study', 'market', 'canteen', 'other']
        for i in range(7):
            feature_name = str("mean_of_" + name_tag[i])
            self.feature_name = feature_name
            FeatureCalculater.cluster(self, clusters=4)
        for i in range(7):
            feature_name = str("median_of_" + name_tag[i])
            self.feature_name = feature_name
            FeatureCalculater.cluster(self, clusters=4)
        for i in range(7):
            feature_name = str("var_of_" + name_tag[i])
            self.feature_name = feature_name
            FeatureCalculater.cluster(self, clusters=4)


class total_amount_every_type(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self)

    @my_exception_handler
    def calculate(self):
        '''
                计算每种消费的总额
        '''
#         sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,sum(abs(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m'),type order by student_num,DATE_FORMAT(date, '%Y-%m')"
        sql = "select student_num,DATE_FORMAT(date, '%Y-%m'),type,sum(abs(transaction_amount)) from card group by student_num,DATE_FORMAT(date, '%Y-%m'),type order by student_num,DATE_FORMAT(date, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        count = [0, 0, 0, 0, 0, 0, 0]
        student_num = result[0][0]
        count_num = 0
        flag = 0
        name_tag = ['charge', 'exercise', 'snack', 'study', 'market', 'canteen', 'other']
        tag = 0
        num = 0
        month_tag = 0
        year_tag = 2200
        year = 2000
        first = 2
        result[0][1].split('-')
        if int(result[0][1][5:7]) < 9:
            num = 1
            first = 1
        for re in result:
            re[1].split('-')
            month = int(re[1][5:7])
            year2 = int(re[1][0:4])
            if re[0] != student_num:
                flag = 2
                num = 0
                first = 2
            elif int(year2) > int(year_tag) and month_tag < 9 and flag != 2:
                year = year_tag - 1
                student_num2 = str(student_num) + (str)(year)
                count = self.SQL_deal(name_tag, count, student_num2)
                count_num += 1
                tag = 1
                first = 2
            elif int(year2) > int(year_tag) and month_tag >= 9 and month >= 9 and flag != 2:
                year = year_tag
                student_num2 = str(student_num) + (str)(year)
                count = self.SQL_deal(name_tag, count, student_num2)
                count_num += 1
                tag = 1
                first = 2
            elif month >= 9 and flag != 2:
                if first == 1:
                    first = 2
                if tag == 0 and num != 0 and first == 0:
                    year = int(re[1][0:4]) - 1
                    student_num2 = str(student_num) + (str)(year)
                    count = self.SQL_deal(name_tag, count, student_num2)
                    count_num += 1
                    tag = 1
                    first = 2
            
            if re[0] == student_num:
                if str(re[2]) == 'other':
                    count[6] += int(re[3])
                elif str(re[2]) == 'canteen':
                    count[5] += int(re[3])
                elif str(re[2]) == 'market':
                    count[4] += int(re[3])
                elif str(re[2]) == 'study':
                    count[3] += int(re[3])
                elif str(re[2]) == 'snack':
                    count[2] += int(re[3])
                elif str(re[2]) == 'exercise':
                    count[1] += int(re[3])
                else: 
                    count[0] += int(re[3])
            if flag == 2:
                if month_tag < 9:
                    year = int(year_tag) - 1
                else:
                    year = int(year_tag)
                student_num2 = str(student_num) + (str)(year)
                count = self.SQL_deal(name_tag, count, student_num2)
                count_num += 1
                flag = 0
                year_tag = int(re[1][0:4])
            month_tag = int(re[1][5:7])
            year_tag = int(re[1][0:4])
            if month < 7 and first == 2:
                tag = 0
                num = 1
                first = 0
            student_num = re[0]

    def SQL_deal(self, name_tag, count, student_num):
        if student_num is None:
            pass
        else:
            for i in range(7): 
                name = str(name_tag[i] + '_total_amount')
                sql = "update students set {0}={1} where student_num='{2}'"
                num = self.executer.execute(sql.format(name, float(count[i]), str(student_num)))
                if num == 0:
                    self.add_student(student_num)
                    self.executer.execute(sql.format(name, float(count[i]), str(student_num)))     
                count[i] = 0

        return count

    def cluster(self):
        name_tag = ['charge', 'exercise', 'snack', 'study', 'market', 'canteen', 'other']
        for i in range(7):
            feature_name = str(name_tag[i] + '_total_amount')
            self.feature_name = feature_name
            FeatureCalculater.cluster(self, clusters=4)

                
class transaction_times(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='transaction_times')

#     @my_exception_handler
#     def calculate(self):
#         sql="SELECT student_num,DATE_FORMAT(date, '%Y-%m'),count(*) from card group by student_num,DATE_FORMAT(date, '%Y-%m') order by student_num"
#         self.executer.execute(sql)
#         result = self.executer.fetchall()
#         print(result)
#         student_num = result[0][0]
#         month_tag = 0
#         month_flag=0
#         year_tag = result[0][0][3:7]
#         count=0
#         for re in result:
#             re[1].split('-')
#             month = int(re[1][5:7])
#             year2 = int(re[1][0:4])
#             if re[0] != student_num:
#                 if int(re[0][3:7])==year2 and month<9:
#                     month_tag=1
#                 else:
#                     month_tag=0
#                 sql="update students set transaction_times=%s where student_num=%s"
#                 num=self.executer.execute(sql, (float(count), str(student_num)+str(year_tag)))
#                 student_num=re[0]
#                 year_tag=re[0][3:7]
#                 count=0
#             #入学第一学年在9月之前有数据的学生，将9月之前的数据归到第一学年
#             if year2!=int(year_tag) and month_tag==1 and month<9:
#                 count+=int(re[2])
#             elif month_tag==1 and month>=9 and year2!=int(year_tag):
#                 sql="update students set transaction_times=%s where student_num=%s"
#                 num=self.executer.execute(sql, (float(count), str(student_num)+str(year_tag)))
#                 year_tag=year2
#                 count=0
#                 count+=int(re[2])
#                 month_tag=0
#             elif year2==int(year_tag) and month_tag==1:
#                 count+=int(re[2])
#                 
#                 
#             #入学第一学年在9月之后有数据的学生,第二学年开始都是跑这个部分
#             elif month_tag==0 and month>=9 and year2==int(year_tag):
#                 count+=int(re[2])
#             elif month_tag==0 and month<9 and year2!=int(year_tag):
#                 count+=int(re[2])
#             elif month_tag==0 and month<9 and year2>int(year_tag)+1:
#                 sql="update students set transaction_times=%s where student_num=%s"
#                 num=self.executer.execute(sql, (float(count), str(student_num)+str(year_tag)))
#                 count=0
#                 count+=int(re[2])
#                 year_tag=year2-1
#                 month_tag=0
#             elif month_tag==0 and month>=9 and year2!=int(year_tag):
#                 if count!=0:
#                     sql="update students set transaction_times=%s where student_num=%s"
#                     num=self.executer.execute(sql, (float(count), str(student_num)+str(year_tag)))
#                 count=0
#                 count+=int(re[2])
#                 year_tag=year2
#                 month_tag=0
    @my_exception_handler
    def calculate(self):
        '''
                            计算总消费次数
        '''
#         print("start")
        """
        下面几行注释掉的是计算最后一个学年数。现有的数据是2016，所以硬编码给出了，跑一遍太费时了。
        """
#         sql = 'select max(date) from card'
#         self.executer.execute(sql)
#         lastestItem_date = self.executer.fetchone()[0]
#         if lastestItem_date.month < 9:
#             lyear = lastestItem_date.year - 1
#         else:
#             lyear = lastestItem_date.year
        lyear = 2016
        sql = "select distinct(student_num) from card"
        self.executer.execute(sql)
        e = self.executer.fetchall()
         
        for i in e:
            stu_num = str(i[0])
            grade = int(stu_num[3:7])
             
            '''
            先处理第一年的特殊情况
            '''
            year1 = grade
            year2 = year1 + 1
            sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-07-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 

            self.executer.execute(sql)
            count = self.executer.fetchone()[0]
#                 
            sql = "update students set transaction_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
#                 
            self.executer.execute(sql)
 
            if count == 0:
                print("计算总消费次数这个学生这个学年可能有问题：" + stu_num + "  " + str(year1))
#                  
            for year1 in range(grade + 1, lyear + 1):
                year2 = year1 + 1
                sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 

                self.executer.execute(sql)
                count = self.executer.fetchone()[0]

                sql = "update students set transaction_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
                
                self.executer.execute(sql)

                if count == 0:
                    print("计算总消费次数这个学生这个学年可能有问题：" + stu_num + "  " + str(year1))

#         print("ok")
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
