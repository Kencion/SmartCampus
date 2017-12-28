'''
Created on 2017年12月28日

@author: 95679
'''
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from math import isnan,isinf
from wordcloud import WordCloud, STOPWORDS

class word_cloud:
    '''
    疑问：以下所有变量前都要加self吗？
    '''
    def __init__(self):
        pass
    
    
    def wordcloud(self,t):
        
        #获取当前路径
        d = path.dirname(__file__)
#         print(d)
#         print(d[:-len('\background_program\visualization')-1])
        text = ""       
        sum = 0.0       
        
        #计算分母sum
        for i in t:
            if not isnan(t[i]) and not isinf(t[i]):
                sum += t[i]
        
        #计算各项特征所占的比例，取小数点后四位精度
        for i in t:
            if isnan(t[i]) or isinf(t[i]):
                t[i] = 0
            else:
                t[i] = int(t[i]/sum *10000)
        
        #根据所占的比例生成text，比例越高出现的次数越多
        for i in t :
            for j in range(t[i]):
                text = text + "," + i
               
        '''
                这边以后要实现不同形状的词云？不止alice这一形状
        '''
        #读取模板图片alice
        alice_mask = np.array(Image.open(path.join(d, "alice.png")))  
        stopwords = {','}
             
        wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
                       stopwords=stopwords)
        
        wc.generate(text)
         
        # 存储图片文件以供调用
        wc.to_file(path.join(d[:-len('\background_program\visualization')-1], "teacher_client\static\\teacher_client\images\WordCloud.png"))
         
        # show
#         plt.imshow(wc, interpolation='bilinear')
#         plt.axis("off")
#         plt.show()
    
