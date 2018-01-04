'''
Created on 2017年12月29日

@author: yzh
'''

import matplotlib.pyplot as plt
import numpy as np
import sys


def broken_line_chart():
    """
    @author:yzh
    @modify: jack把这个函数的名字由zhexian_fig改成了 broken_line_chart
    @return: 填一下
    """
    from background_program.y_Modules.class_failing_warning import class_failing_warning
    
    t = class_failing_warning()
    infos = t.doit()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 4., 1.01 * height, "%s" % float(height))

    num = np.zeros(5)
    score = [x[1] for x in infos]
     
    for i in range(5):
        num[i] = score.count(i)
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ax.set_title('Bar Chart')
    colors = ['red', 'yellowgreen', 'lightskyblue', 'g', 'b']
    labels = [u"0类", u"1类", u"2类", u"3类", u"4类"]
    rec = plt.bar(labels, num, color=colors) 
    autolabel(rec)
    ax.set_xlabel('Student type')
    ax.set_ylabel('Student number')
    save_path = sys.path[0] + '/teacher_client/static/teacher_client/images/broken_line_chart.png'
    plt.savefig(save_path)
    plt.close()

 
def pie_chart():
    """
    @author: yzh
    @modify: jack把这个函数的名字由bingzhuang_fig改成了 pie_chart
    @return: 填一下
    """
    from background_program.y_Modules.class_failing_warning import class_failing_warning
    t = class_failing_warning()
    infos = t.doit()
#     print(infos)
    num = np.zeros(5)
    colors = ['red', 'yellowgreen', 'lightskyblue', 'g', 'b']
    labels = [u"0类", u"1类", u"2类", u"3类", u"4类"]
    score = [x[1] for x in infos]
    for i in range(5):
        num[i] = score.count(i)
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ax.set_title('Pie Chart')
    patches, l_text, p_text = plt.pie(num, labels=labels, colors=colors, labeldistance=1.1, autopct='%3.1f%%', shadow=False, startangle=90, pctdistance=0.6) 
    save_path = sys.path[0] + '/teacher_client/static/teacher_client/images/pie_chart.png'
    for t in l_text:
        t.set_size = (30)
    for t in p_text:
        t.set_size = (20)
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.legend()
    plt.savefig(save_path)
#     plt.show()
    plt.close()

    
def line_chart():
    """
    @author: yzh
    @return: 填一下
    """
    from background_program.y_Modules.score_forcasting import score_forcasting
    
    t = score_forcasting()
    infos = t.doit()
    
    score = [x[1] for x in infos]
    x = range(101)
    y = np.zeros(101)
    for i in x:
        for j in score:
            if j >= (i - 0.5) and j < (i + 0.5):
                y[i] += 1
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ticks = ax.set_xticks(np.linspace(0, 100, 21))
    plt.xlim(0, 100)
    ax.set_title('学生成绩分布折线图')
    ax.set_xlabel('成绩')
    ax.set_ylabel('学生数量')
    plt.ylim(0, max(y) * 1.1)
    ax.plot(x, y, linewidth=2 , color='#436EEE') 
    
    ax.fill(x, y, color='#00B2EE')
    save_path = sys.path[0] + '/teacher_client/static/teacher_client/images/line_chart.png'
    plt.legend()
    plt.savefig(save_path)
    # plt.show()
    plt.close()

