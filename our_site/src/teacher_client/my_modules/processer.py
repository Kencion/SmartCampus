'''
Created on 2018年1月7日

@author: Jack
'''

from django.shortcuts import loader
import json


class data_page_processer():
    '''
    combine data and page
    '''

    def get_feature_scores_and_ranges_page(self, feature_scores_and_ranges, request):
        '''
        @param feature_scores_and_ranges: 
        @return: feature_scores_and_ranges_page
        '''

        feature_scores_and_ranges_page = loader.get_template(
            'teacher_client/charts/feature_scores_and_ranges.html')
        context = {'result': json.dumps(feature_scores_and_ranges)}

        return feature_scores_and_ranges_page.render(context, request)

    def get_pie_page(self, chart_name, my_data, request):
        '''
        @param chart_name: 
        @param my_data: 
        @return: pie_page
        '''
        pie_page = loader.get_template('teacher_client/charts/pie_chart.html')
        context = {
            'chart_name': chart_name,
            'my_data': my_data,
        }

        return pie_page.render(context, request)


class data_processer():
    '''
    process ge zhong ge yang data
    '''

    def __init__(self, module_name, dj_module, bk_module):
        '''
        @param dj_module: django module
        @param bk_module: background module 
        '''
        self.module_name = module_name
        self.dj_module = dj_module
        self.bk_module = bk_module()

    def get_evaluate_score(self, data_update=False):
        '''
        获取成绩预测模块可信度分数
        @return evaluate_score
        '''
        evaluate_score = 0

        if data_update:
            evaluate_score = self.bk_module.get_evaluate_score()
            self.dj_module.objects.filter(module_name=self.module_name).update(
                evaluate_score=evaluate_score)
        else:
            try:
                evaluate_score = self.dj_module.objects.filter(
                    module_name=self.module_name)[0].evaluate_score
            except:
                evaluate_score = self.bk_module.get_evaluate_score()
                self.dj_module.objects.filter(module_name=self.module_name).update(
                    evaluate_score=evaluate_score)

        return evaluate_score

    def get_tree_data(self):
        '''
        数据的转换，转成echarts树形图能识别的格式
        @author: yzh
        @return: data,json格式
        '''
        import operator

        features_range = self.bk_module.get_features_range()
        data = {}
        name = 'name'
        children = 'children'
        value = 'value'
        list2 = []
        
        # 获得当前类名
        data[name] = ''
        
        # 获得特征的评分并对特征按照评分进行排序
        feature_scores = sorted(self.bk_module.get_feature_scores().items(), key=operator.itemgetter(1))
        
        # 取评分前十个存储
        for d_index in range(len(feature_scores) - 10, len(feature_scores)):
            list1 = []
            dic2 = {}
            dic2[name] = feature_scores[d_index][0]
            if feature_scores[d_index][1] == float("inf"):
                dic2[value] = 9999
            else:
                dic2[value] = float(feature_scores[d_index][1])
            for i in features_range[feature_scores[d_index][0]]:
                dic1 = {}
                dic1[name] = str(i) + ":" + str(features_range[feature_scores[d_index][0]][i])
                list1.append(dic1)

            dic2[children] = list1
            list2.append(dic2)

        data[children] = list2

        return data

    def get_pie_data(self, counter, condition, data_update=False):
        """
        获得成绩预测饼图数据
        @return pie_data
        """

        if data_update:
            pie_data = self.get_pie_datas(counter, condition)
            self.dj_module.objects.filter(
                module_name=self.module_name).update(pie_data=pie_data)
        else:
            try:
                pie_data = eval(self.dj_module.objects.filter(
                    module_name=self.module_name)[0].pie_data)
            except:
                pie_data = self.get_pie_datas(counter, condition)
                self.dj_module.objects.filter(
                    module_name=self.module_name).update(pie_data=pie_data)

        return pie_data

    def get_pie_datas(self, counter, condition):
        '''
        获得echarts画饼图需要的数据
        @params
        @retrun data:list
        '''
        def is_between(value, min_value, max_value):
            if value >= min_value and value < max_value:
                return True
            return False

        the_list = [x[1] for x in self.bk_module.predict()[1]]
        print(condition)
        for i in the_list:
            for ct, cd in zip(counter, condition):
                if is_between(i, cd[0], cd[1]):
                    counter[ct] += 1
                    break
        print(the_list)
        pie_data = []
        for name in counter:
            dic = {
                'name': name,
                'value': counter[name], }
            pie_data.append(dic)
        print(pie_data)
        return pie_data

    def get_feature_scores_and_ranges(self, data_update=False):
        """
        获得90分以上、60分以下的学生的特征范围
        @return feature_scores_and_ranges
        """

        if data_update:
            f_s_and_r = self.get_tree_data()
            self.dj_module.objects.filter(module_name=self.module_name).update(
                feature_scores_and_ranges=f_s_and_r)
        else:
            try:
                f_s_and_r = eval(self.dj_module.objects.filter(
                    module_name=self.module_name)[0].feature_scores_and_ranges)
            except:
                f_s_and_r = self.get_tree_data()
                self.dj_module.objects.filter(module_name=self.module_name).update(
                    feature_scores_and_ranges=f_s_and_r)

        return f_s_and_r
