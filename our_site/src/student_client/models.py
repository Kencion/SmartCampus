from django.db import models

# Create your models here.
class Student(models.Model):
    student_num = models.CharField(max_length=20, default='student_num')
    student_name = models.CharField(max_length=50, default='student_name')
    score = models.FloatField(max_length=10, default=0.0)
