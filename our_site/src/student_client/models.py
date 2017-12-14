from django.db import models
from datetime import datetime

# Create your models here.
class Student(models.Model):
    student_num = models.CharField(primary_key=True, max_length=50, editable=False)
    student_name = models.CharField(max_length=50, default='student_name')
    score = models.FloatField(max_length=10, default=0.0)
    is_missing = models.BooleanField(default=False)
    have_scholarship = models.BooleanField(default=False)
    have_subsidy = models.BooleanField(default=False)
    update_time = models.DateTimeField(default=datetime.now(), blank=True)
    
    def get_by_student_num(self):
        pass
    
    def get_students_who_are_missing(self):
        pass
    
    def get_students_who_have_scholarship(self):
        pass
    
    def get_students_who_have_subsidy(self):
        pass
