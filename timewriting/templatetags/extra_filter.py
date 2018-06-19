'''
Created on 16.06.2018

@author: makki
'''
from django import template
import datetime

register = template.Library()
#register.filter('schneide', cut)

@register.filter('schneide')
def cut(value, arg):
    return value.replace(arg,'###')

@register.filter('addseven')
def addseven(indate):
    return indate+datetime.timedelta(7)

@register.filter('subseven')
def subseven(indate):
    return indate+datetime.timedelta(-7)

