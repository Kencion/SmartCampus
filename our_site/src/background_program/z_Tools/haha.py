'''
Created on 2017年12月11日

@author: Jack
'''
import pip
from subprocess import call

for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)