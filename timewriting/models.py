from django.db import models
from django.conf import settings
import re, datetime
User = settings.AUTH_USER_MODEL

# Create your models here.
class TimePlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    location1 = models.CharField(max_length=30, null=False, blank=True)
    location2 = models.CharField(max_length=30, null=False, blank=True)
    
    def __str__(self):
        return str(self.entry_id)+'|'+str(self.start_time)+'|'+str(self.end_time)+'|'+str(self.location1)+'|'+str(self.location2)
    
    def create(self,user,start,end,loc1,loc2):
        self.user=user
        self.start_time=start
        result=re.match(r'(\d{4})-(\d{2})-(\d{2})',self.start_time)
        year, month, day =(result.group(1),result.group(2),result.group(3))
        if(len(TimePlot.objects.filter(start_time__year=year,start_time__month=month,start_time__day=day).filter(user=user))>0):
            return False
        
        self.end_time=end
        self.location1=loc1
        self.location2=loc2
        self.save()
        return True