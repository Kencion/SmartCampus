'''
Created on 2017年11月21日
 
@author: jack
'''
 
from FeatureCalculaters.library import * 
from FeatureCalculaters.scholarship import *
from FeatureCalculaters.subsidy import *
from FeatureCalculaters.score import *
from tqdm import tqdm
 
claculaters = [library_study_time.library_study_time(),
            library_week_study_time.library_week_study_time(),
            scholarship_amount.scholarship_amount(),
            scholarship_rank.scholarship_rank(),
            subsidy_amount.subsidy_amount(),
            subsidy_rank.subsidy_rank(),
            GPA.GPA(),
            score.score()
    ]
 
for claculater in tqdm(claculaters):
    claculater.calculate()
     
# 关闭数据库
for claculater in tqdm(claculaters):
    claculater.afterCalculate()

