'''
Created on 18.06.2018

@author: makki
'''
import datetime
from .models import TimePlot

def getWeekWorkSum(start_time,user):
    #print('Input'+str(start_time))
    weekday=start_time.weekday()
    stepsadd=6-weekday
    firstday=(start_time-datetime.timedelta(weekday)).date()
    #firstday=firstday.replace(hour=0,minutes=0)
    lastday=(start_time+datetime.timedelta(stepsadd+1)).date()
    #lastday=lastday.replace(hour=23,minutes=59)
    #print('first:',firstday)
    #print('last:',lastday)
    queryset = TimePlot.objects.filter(user=user).filter(start_time__gt=firstday).filter(end_time__lt=lastday)
    #print(queryset)
    timedeltas=[]
    ids=[]
    
    for entry in queryset:
        ids.append(entry.entry_id)
        timedeltas.append(entry.end_time-entry.start_time)
    xsum=0
    #print(len(timedeltas))
    for x in timedeltas:
        xsum+=x.seconds
    return xsum/3600, ids

def getMonthWorkSum(start_time, user):
    month = start_time.month
    year = start_time.year
    ids=[]
    timedeltas=[]
    
    queryset = TimePlot.objects.filter(user=user).filter(start_time__year=year).filter(start_time__month=month)
    
    for entry in queryset:
        ids.append(entry.entry_id)
        timedeltas.append(entry.end_time-entry.start_time)
    xsum=0
    #print(len(timedeltas))
    for x in timedeltas:
        xsum+=x.seconds
    return xsum/3600, ids