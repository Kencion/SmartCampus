'''
Created on 2018年4月11日

@author: xmu
'''
from background_program.b_Sample_processing.Feature_calculating import FeatureCalculater
def update_dataSet():
        '''
        更新表‘students2’与钱有关的部分列
        将null更新成0
       
        '''
        """确定label是哪一列，并将其作为待预测对象"""
        dataset =FeatureCalculater.FeatureCalculater()
        dataset.executer.execute("DESCRIBE students2")
        columnName = dataset.executer.fetchall()
        index = -1
        for i in range(len(columnName)):
            if str(columnName[i][0]) == 'canteen_total_amount' :
                index = i
                break
        if index == -1:
            print('异常：未发现' + 'canteen_total_amount')
        
        for  i in range(index,len(columnName)):
            sql = 'update students2 set  {0}=0 where {1} is null'
            print(sql.format(columnName[i][0], columnName[i][0]))
            dataset.executer.execute(sql.format(columnName[i][0], columnName[i][0]))
update_dataSet()      
