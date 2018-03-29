'''
Created on 2017年11月21日
@author: jack
'''
class Student():
    '''
              学生类，要画像的对象
    '''
    def __init__(self, student_num, features=None, label="1"):
        self.student_num = student_num
        try:
            self.features = list(features)
        except:
            pass
        self.label = label
        
    def setStudent_num(self, student_num): 
        '''
                        设置学号
        @params string student_num:学生学号           
        @retrun
        '''
        self.student_num = student_num
    
    def getStudent_num(self):
        '''
                        获取学号
        @params 
        @retrun string self.student_num:学生学号
        '''
        return self.student_num
        
    def getAll(self):
        '''
                        返回特征+标签
        @params 
        @retrun list[[]] features_and_labels:[特征,标签]
        '''
        features_and_labels=self.features+[self.label]
#         print(features_and_labels)
        return features_and_labels
    '''
        用于特征工程，根据记录删除对应的特征属性，返回新的数据集和特征属性名
        @params labels int 要删除的列的下标,X_test nparray.mat 测试数据集
        @retrun X_test nparray.mat 测试数据集
        list转换成mat:numpy.mat(list)
        mat转换成list:mat.tolist()
        '''
    def get_New_Xtest(self,labels,X_test):
        import numpy as np
        #b=X_test.tolist()
        b=X_test
        row=[[] for i in range(len(b[0])-len(labels))]
        num=0
        for k in range(len(b[0])):
            for i in range(len(b[1])):
                for j in labels:
                    if i!=j:
                       row[num].append(b[k][i])
        print(row)
#         b = list([[row[i] for i in range(len(b[1])) if i != label] for row in b] )
#         New_Xtest=np.mat(b)
#         with open(r"new_feature_name") as f: # 需要重新打开文本进行读取
#             content=[]
#             count=0
#             for line2 in f:
#                 for i in labels:
#                     if count==i:
#                         pass
#                     else:
#                         content.append(line2.rstrip())
#                 count=count+1
#         with open(r"new_feature_name",'w') as f: 
#             for line in content:
#                 f.write(line+'\n')
#             f.close()
#         return New_Xtest
# if __name__=="__main__":
# #     print(features_name_en[0])
#     stu=Student("24320142202524","student_num")
#     X_test=[[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]]
#     labels=[0]
#     stu.get_New_Xtest(labels,X_test)
