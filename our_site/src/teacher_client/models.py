from django.db import models


class my_module(models.Model):
    module_name = models.CharField(primary_key=True, max_length=50)
    feature_scores_and_ranges = models.CharField(max_length=9999)
    pie_data = models.CharField(max_length=9999)
    
