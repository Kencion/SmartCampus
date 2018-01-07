'''
Created on 2018年1月7日

@author: Jack
'''


def yzh_data_process():
    pass


def get_feature_scores_and_ranges_page(feature_scores_and_ranges, request):
    from django.shortcuts import loader
    import json
    
    feature_scores_and_ranges_page = loader.get_template('teacher_client/feature_scores_and_ranges.html')
    
    context = {'result':json.dumps(feature_scores_and_ranges)}
    
    return feature_scores_and_ranges_page.render(context, request)
                            
