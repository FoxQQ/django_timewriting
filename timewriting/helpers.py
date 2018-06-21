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
    todayid=None
    ids=[]
    timedeltas=[]
    today=datetime.datetime.now()
    queryset = TimePlot.objects.filter(user=user).filter(start_time__year=year).filter(start_time__month=month)
    
    for entry in queryset:
        ids.append(entry.entry_id)
        timedeltas.append(entry.end_time-entry.start_time)
        
    xsum=0
    #print(len(timedeltas))
    for x in timedeltas:
        xsum+=x.seconds
    return xsum/3600, ids

def populateWeek(user, start_time, end_time, loc1, loc2):
    
    print('given to function:',start_time, end_time, loc1, loc2)
    start_time=datetime.datetime.strptime(start_time,'%Y-%m-%dT%H:%M')
    end_time=datetime.datetime.strptime(end_time,'%Y-%m-%dT%H:%M')
    weekday=start_time.weekday()
    firstday=(start_time-datetime.timedelta(weekday))
    for i in range(7):
        iday=firstday+datetime.timedelta(i)
        if(len(TimePlot.objects.filter(user=user).filter(start_time__year=iday.year,start_time__month=iday.month,start_time__day=iday.day))>0):
            continue
        else:
            entry=TimePlot()
            start=iday
            end=iday
            if(i<5):
                start=start.replace(hour=start_time.hour,minute=start_time.minute)
                end=end.replace(hour=end_time.hour,minute=end_time.minute)
            else:
                start=start.replace(hour=0,minute=0)
                end=end.replace(hour=0,minute=0)
                print('weekend',start)
                
            entry.create(user, str(start), str(end), loc1, loc2)
    
    
    