'''
Created on 2018年1月9日

@author: YHJ
'''
from django.shortcuts import loader
import json
def get_students_info(students_info, request):
    students_info_page = loader.get_template('student_client/chart_cloudword/student_info.html')
    context = {'result':json.dumps(students_info)}
    return students_info_page.render(context, request)

