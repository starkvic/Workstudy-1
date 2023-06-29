from django.contrib import messages
from django.http import  HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import (
    CreateView,DetailView,UpdateView,ListView
)
from django.db.models import Q,F
from .models import Workday,User,Job,Workarea,Application
from django.utils import timezone
import datetime
from django.utils.timezone import localtime
from django.views.generic import dates
from collections import Counter
from django.core.exceptions import ValidationError

def logout_user(request):
    logout(request)
    return redirect('home')
def create_job_application(request,job_id):
    if request.method == "POST":
        user = get_object_or_404(User,user_id=request.user.user_id)
        job = get_object_or_404(Job,id=job_id)
        alread_applied = Application.objects.filter(Q(job=job)&Q(user=user))
        if alread_applied.exists():

            messages.warning(request,f"{user} has already applied for this job!",extra_tags="warning")
            return redirect('.')
        Application.objects.create(
            user = user,
            job=job,
        )
        messages.success(request,"Your application was successful!")
        return redirect('home')
    return render(request,"cutomuser/job_application.html")


def generator(n):
    #initialize the counter value 
    value = 0
    #Loop until the counter is less than n
    while value <n:
        #produce the current value of the counter
        yield value

        #increment the counter 
        value +=1
import random
statuses = [
    'pending','process','completed'
]

class ArticleTodayArchiveView(LoginRequiredMixin,dates.DayArchiveView):
    queryset = User.objects.all()
    date_field = "date_created"
    allow_future = True

# def check_in_and_out_time(time):
#     return (time - (day_beginning(None)+datetime.timedelta(hours=6)))>=datetime.timedelta(hours=10)
# def homeview(request):
#     current_time = timezone.now()
#     if check_in_and_out_time(current_time):
#         context = {'day_beginning':day_beginning()+datetime.timedelta(hours=6)}
#     return render(request,"cutomuser/home.html",context)





class General_Create_View(CreateView):
    jobs=Job.objects.all()
    def post(self, request, *args, **kwargs):
      return super().post(request, *args, **kwargs)

class JobAppllicationView(LoginRequiredMixin,CreateView):
    success_url = reverse_lazy('home')
    def form_valid(self,class_form):
        return super().form_valid(class_form)
    
    
    
class WorkareaView(LoginRequiredMixin,DetailView):
    success_url = reverse_lazy('workarea')
    def get_object(self):
        return get_object_or_404(self.model,pk=self.kwargs.get('pk'))
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        workarea = self.get_object()
        context['members'] =workarea.members.all()
        context['jobs'] =Job.objects.all()
        return context



    
class HomeView(ListView):
    q=None
    myid=0
    workdays = Workday.objects.all()
    def get_queryset(self, **kwargs):
        return (self.model.objects.filter(created__lte = timezone.now())[:5])
    def get(self, request, *args, **kwargs):
        self.q=request.GET.get('q') if request.GET.get('q') != None else ''
        return super().get(request, *args, **kwargs)
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        workareas = Workarea.objects.filter(
                                Q(job__job_title__icontains=self.q)|
                                Q(name__icontains=self.q)
                                )
        context['jobs'] =Job.objects.all()

        
        applications = {}
        try:
            applications = Counter([i.job.job_title for i in Application.objects.all()])
        except:
            pass
        context['applications_per_job_dict'] =dict(applications)
        context['workareas'] =workareas
        context['statuses'] = random.shuffle(statuses)
        context['colors']=['meter animate','meter  orange nostripes','meter','meter  red nostripes','meter  blue nostripes','meter  pink nostripes']
        context['workdays'] =Workday.objects.filter(Q(workarea__job__job_title__icontains=self.q,archived = False))
        if self.workdays.count() > 0 :
            if self.workdays.first().check_in == False:
                context["check_in"]=True
        return context
    def post(self, request, *args,**kwargs) :
        check,workarea_id = request.POST['check_in'].split('-')
        now=timezone.localtime(timezone.now())
        begin = Workday.day_beginning()
        still_today = Workday.days_hours_minutes(now-(begin+datetime.timedelta(hours=8)))
        end =begin + datetime.timedelta(hours =18)
        self.workdays = Workday.objects.all()
        if check and now > begin+datetime.timedelta(hours=8) and now.weekday()<5 and still_today['days']==1:
           if self.workdays.count()> 0:
               self.myid=F('id')+1
           else:
               self.myid = 1 
            #When creating a new workday, archive all the previous workdays so that we can filter the latest
           unarchived_days = Workday.objects.filter(created__lt=begin+datetime.timedelta(hours=8)) 
           if unarchived_days:
               for i in unarchived_days:
                   i.archived =True

           workarea = Workarea.objects.get(id=workarea_id)
           workday= Workday.objects.create(
                 id=1,
                check_in =True,
                user = request.user,
                workarea = workarea
            )
           workday.save()
           return redirect('home')
        elif not check and now<end:
            workday = Workday.objects.all().first()
            workday.check_out =True
            workday.check_in = False
            workday.time_out = timezone.now()
            workday.save()
            return redirect('home')
        elif not now > begin+datetime.timedelta(hours=8):
            messages.warning(request,f"You can Check in only from 8:00 am")
            return redirect('.')
        elif not now.weekday()<5:
            messages.warning(request,f"Weekend is not a working time! Rest!")
            return redirect('.')
        else:
            messages.warning(request,f"Just Wait, You cannot check in twice")
            return redirect('.')
    



class UserProfileView(LoginRequiredMixin,DetailView):
    q=None
    def get_object(self, **kwargs):
        return get_object_or_404(self.model,pk=self.kwargs.get('pk'))
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        workareas = user.workarea_set.all()
        context['jobs'] =Job.objects.all()
        context['workareas'] =workareas
        context['self.workdays'] =Workday.objects.filter(Q(workarea__job__job_title__icontains=self.q))
        return context

class NewUserView(SuccessMessageMixin,CreateView):
    success_url = reverse_lazy('login')
    success_message = "%(email)s , your registration was successful"


    

