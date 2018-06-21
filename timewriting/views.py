from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import TimePlotForm
from django.template import loader
from .models import TimePlot
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import numpy as np
from timewriting import helpers
def simpleResponse(request):
    response=""
    '''response += request.scheme+"<br>"
    response += str(request.body)+"<br>"
    response += request.path+"<br>"
    response += request.path_info+"<br>"
    response += request.method+"<br>"
    response += str(request.GET.keys())+"<br>"
    response += str(request.COOKIES)+"<br>"
    '''
    response += str(request.user)+"<br>"
    
    response+=str(TimePlot.objects.filter(start_time__year=2018))
    print(TimePlot.objects.filter(start_time=datetime.date(2018,6,15)))
    #for key, val in request.META.items():
    #    response += key+":"+str(val)+"<br>"
    
    
    return HttpResponse(response)

'''class addDayView(TemplateView):
    template_name='timewriting/add_day.html'
    
    def post(self, request, *args, **kwargs):
        print(request)
        return FormView.post(self, request, *args, **kwargs)
'''    
class addDayView(FormView):
    template_name='timewriting/add_day.html'
    form_class = TimePlotForm
    success_url = 'timewriting/view_entry.html'
    
    def form_invalid(self, form):
        print("INVALID")
        print(form)
        return FormView.form_invalid(self, form)
    
    def form_valid(self, form):
        print(form)
        return FormView.form_valid(self, form)
   
def homeView(request):
    
    template=loader.get_template('timewriting/home.html')
    context={}
    return HttpResponse(template.render(context, request))
    
@login_required(login_url='login')
def add_day(request):
    template=loader.get_template('timewriting/add_day.html')
    context={}
    if('edit' in request.GET and request.GET['edit'].isdigit()):
        id = request.GET['edit']
        
        context['entry']=TimePlot.objects.get(entry_id=id)
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def statistics_view(request):
    template = loader.get_template('timewriting/statistics.html')
    context = {}
    user=request.user
    data = TimePlot.objects.filter(user=user).order_by('start_time')
    
    xaxis = [(x.start_time.strftime("%d.%m.%Y")) for x in data]
    yaxis = [(y.end_time-y.start_time).seconds/3600 for y in data]
    print(xaxis)
    context['xdata']=xaxis
    context['ydata']=yaxis
    data=np.array(yaxis)
    mask=data>0
    data=data[mask]
    if(len(data)>0):
        context['avg']=np.average(data)
        context['max']=np.max(data)
        context['min']=np.min(data)
        context['std']=np.std(data)
    
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def show_days(request):
    template=loader.get_template('timewriting/your_days.html')
    user=request.user
    context={}
    print('POST Message: ', request.POST)
    print('GET Message: ', request.GET)
    if(request.method == 'POST' and 'submit' in request.POST):
        user=request.user
        start_time=request.POST['start_time']
        end_time=request.POST['end_time']
                
        if(request.POST['loc1']):
            loc1=request.POST['loc1']
        else: loc1=""
        if(request.POST['loc2']):
            loc2=request.POST['loc2']
        else: loc2=""
        
        entry= TimePlot()
        if(request.POST['editmode']!='False'):
            entry=TimePlot.objects.filter(entry_id=request.POST['editmode'])
            entry.update(start_time=start_time,end_time=end_time,location1=loc1,location2=loc2)
            context['result']=True
        else:
            result = entry.create(user, start_time, end_time, loc1, loc2)
            context['result']=result
        
    if('day' in request.GET and request.GET['day']!='' and request.GET['day']!='all'):
        day=datetime.datetime.strptime(request.GET['day'],"%Y-%m-%d")
        
    else:
        day=datetime.datetime.today()  
    if('delete' in request.GET):
        try:
            TimePlot.objects.filter(user=user).filter(entry_id=request.GET['delete']).delete()
            context['deleteresult']='success'
        except Exception as e:
            context['deleteresult']=e 
    if('day' in request.GET and request.GET['day']!='all'):
        if('month' in request.GET):
            weeklysum, ids=helpers.getMonthWorkSum(day, user)
        else:
            weeklysum, ids=helpers.getWeekWorkSum(day,user)
        
        context['weeklysum']= weeklysum
        context['ids']=ids
        entries=TimePlot.objects.filter(user=user).filter(entry_id__in=ids).order_by('start_time')
    else:
        entries=TimePlot.objects.filter(user=user).order_by('start_time')
    
    #[entry[x],entry[y]=entry[y],entry[x] for x,y in range(7)]
    context['entries']=entries
    
    today = datetime.datetime.now()
    for entry in entries:
        if(today.day==entry.start_time.day and today.month==entry.start_time.month and today.year==entry.start_time.year):
            context['todayid']=entry.entry_id
    
    #print(context['entries'][0].start_time.weekday())
    #print(context['entries'][0].end_time-context['entries'][0].start_time)
    return HttpResponse(template.render(context, request))

def login_view(request):
    template=loader.get_template('snippets/login.html')
    context={}
    if (request.method == 'POST'):
        username=request.POST['user']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        if (user is not None):
            login(request, user)
            template=loader.get_template('timewriting/home.html')
            
            return HttpResponse(template.render(context, request))
        else:
            context['credentials']=True
            return HttpResponse(template.render(context, request))
    
    return HttpResponse(template.render(context, request))



def logout_view(request):
    logout(request)
    template=loader.get_template('timewriting/home.html')
    context={'logout':True}
    return HttpResponse(template.render(context, request))



def simple(request):
    image_data = open(r"C:\Users\makki\Pictures\image-512.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")
    

    