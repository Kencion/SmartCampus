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
 
    def get_feature_ranges_tree_page(self, feature_scores_and_ranges, request):
        '''
        @param feature_scores_and_ranges:
        @return: feature_scores_and_ranges_page
        '''
 
        feature_scores_and_ranges_page = loader.get_template(
            'teacher_client/charts/feature_ranges_tree_chart.html')
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
     
    def get_feature_ranges_radar_page(self, types, top_10_features, top_10_feature_range, request):
        '''
        @param feature_scores_and_ranges:
        @return: feature_scores_and_ranges_page
        '''
 
        radar_page = loader.get_template(
            'teacher_client/charts/feature_ranges_radar_chart.html')
        context = {'types':json.dumps(types),
                   'top_10_features':json.dumps(top_10_features),
                   'top_10_feature_range':json.dumps(top_10_feature_range),
                   }
 
        return radar_page.render(context, request)
 
 
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
 
    def get_radar_data(self):
         
        # 排名前10的特征名
        top_10_features = self.bk_module.get_feature_scores()[-30:]
            
        top_10_features = [f[0] for f in top_10_features]
         
        features_range = self.bk_module.get_features_range()
         
        # 类别
        types = list(list(features_range.values())[0].keys())
        for t in types[:]:
            types.append(t + '-0')
            types.append(t + '-1')
            types.remove(t)
        
        # 排名前10的特征的范围
        top_10_feature_range = dict()
        for t in types:
            top_10_feature_range[t] = []
            for f in top_10_features:
                top_10_feature_range[t].append(features_range[f][t[:-2]][int(t[-1])])
            
        print(top_10_feature_range)
         
        return  types, top_10_features, top_10_feature_range
 
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
        feature_scores = sorted(
            self.bk_module.get_feature_scores().items(), key=operator.itemgetter(1))
 
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
                dic1[name] = str(
                    i) + ":" + str(features_range[feature_scores[d_index][0]][i])
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
 
            try:
                m = self.dj_module.objects.get(module_name=self.module_name)
            except:
                m = self.dj_module(module_name=self.module_name)
 
            m.pie_data = pie_data
            m.save()
        else:
            try:
                pie_data = eval(self.dj_module.objects.get(
                    module_name=self.module_name).pie_data)
            except:
                pie_data = self.get_pie_data(
                    counter, condition, data_update=True)
        
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
 
        for i in the_list:
            for ct, cd in zip(counter, condition):
                if is_between(i, cd[0], cd[1]):
                    counter[ct] += 1
                    break
 
        pie_data = []
        for name in counter:
            dic = {
                'name': name,
                'value': counter[name], }
            pie_data.append(dic)
        
        return pie_data
 
    def get_feature_scores_and_ranges(self, disp_type, data_update=False):
        """
        获得90分以上、60分以下的学生的特征范围
        @return feature_scores_and_ranges
        """
 
        if data_update:
            if disp_type == 'tree':
                f_s_and_r = self.get_tree_data()
            else:
                f_s_and_r = self.get_radar_data()
            try:
                m = self.dj_module.objects.get(module_name=self.module_name)
            except:
                m = self.dj_module(module_name=self.module_name)
 
            m.feature_scores_and_ranges = f_s_and_r
            m.save()
        else:
            try:
                f_s_and_r = eval(self.dj_module.objects.get(
                    module_name=self.module_name).feature_scores_and_ranges)
            except:
                f_s_and_r = self.get_feature_scores_and_ranges(disp_type, data_update=True)
 
        return f_s_and_r
