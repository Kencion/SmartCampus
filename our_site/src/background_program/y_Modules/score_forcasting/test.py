import matplotlib.pyplot as plt
import numpy as np
import os, sys
from background_program.y_Modules.score_forcasting.score_forcasting import score_forcasting
from numpy import linspace
'''
Created on 2017年12月14日

@author: 95679
'''


t = score_forcasting('score')
infos = t.doit()

score = [x[1] for x in infos]
x = range(101)
y = np.zeros(101)
for i in x:
    for j in score:
        if j>=(i-0.5) and j<(i+0.5):
            y[i]+=1
fig = plt.figure('By SmartCampus Team')
ax = fig.add_subplot(111)
ticks = ax.set_xticks(np.linspace(0,100,21))
plt.xlim(0,100)
ax.set_title('学生成绩分布折线图')
ax.set_xlabel('成绩')
ax.set_ylabel('学生数量')
plt.ylim(0,max(y)*1.1)
ax.plot(x,y,color = 'skyblue') 

ax.fill(x,y,color = 'skyblue')
save_path = sys.path[0] + '/teacher_client/static/teacher_client/images/line_chart.png'
plt.legend()
plt.savefig(save_path)
# plt.show()
plt.close()
