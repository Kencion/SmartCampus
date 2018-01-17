'''
Created on 2018年1月7日

@author: Jack
'''

from django.shortcuts import loader
import json


def yzh_data_process():
    pass


def get_feature_scores_and_ranges_page(feature_scores_and_ranges, request):
    feature_scores_and_ranges_page = loader.get_template('teacher_client/charts/feature_scores_and_ranges.html')
    context = {'result':json.dumps(feature_scores_and_ranges)}
    
    return feature_scores_and_ranges_page.render(context, request)

                            
def get_pie_page(chart_name, my_data, request):
    pie_page = loader.get_template('teacher_client/charts/pie_chart.html')
    context = {
        'chart_name':chart_name,
        'my_data':my_data,
               }
    
    return pie_page.render(context, request)
