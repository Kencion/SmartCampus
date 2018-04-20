'''
Created on 2017年11月20日

@author: jack
'''

# 在这段时间中算晚
timeSlot = "BETWEEN '01:00:00' AND '04:00:00"
# 在外面很晚的次数，高于这个次数就不好
StayOutLateTimes = "5"

# 超过1点出宿舍,并且超过1个小时没回来
m_out_1_not_in_sql = "SELECT DISTINCT(student_num),record_time FROM dorm_entrance WHERE in_out = '出门' AND DATE_FORMAT(record_time, '%H:%i') BETWEEN '01:00' AND '04:30'"
# 超过1点才回宿舍次数超过3次
over_2_in_3_times_sql = "SELECT * FROM ( SELECT student_num,record_time,COUNT(*) AS times FROM dorm_entrance WHERE in_out = '进门' AND DATE_FORMAT(record_time, '%H:%i') BETWEEN '01:00' AND '04:30' GROUP BY student_num ) t WHERE times > 3"
# 在工作日在外时间超过48小时
#
# 一个月record_type未授权超过120次
wrong_time_sql = "SELECT DISTINCT(student_num),record_time FROM (SELECT student_num,record_time,count(record_type = '未授权') AS wrong_time,DATE_FORMAT(record_time, '%Y-%m') AS MONTH FROM dorm_entrance GROUP BY student_num,MONTH) t WHERE wrong_time >= 100"

missing_students = {}


def get_missing_students():
    from background_program.z_Tools.my_database import MyDataBase

    executer = MyDataBase("软件学院").getExcuter()
    sqls_and_reasons = [(m_out_1_not_in_sql, '超过1点出宿舍，并且超过1个小时没回来'),
                        (over_2_in_3_times_sql, '超过1点才回宿舍次数超过3次'),
                        #                          (wrong_time_sql, '一个月record_type未授权超过120次'),
                        ]

    for sql_and_reason in sqls_and_reasons:
        executer.execute(sql_and_reason[0])
        for i in executer.fetchall():
            add_student(student_num=i[0] + str(i[1].year), reason=sql_and_reason[1])

    return missing_students


def add_student(student_num, reason):
    try:
        missing_students[student_num].append(reason)
    except:
        missing_students[student_num] = [reason, ]


if __name__ == '__main__':
    t = get_missing_students()
    for i in t:
        print(i)
