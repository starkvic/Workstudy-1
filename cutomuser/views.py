from typing import Any, Dict, Optional
from django.db import models
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import (
    CreateView,DetailView,UpdateView,ListView
)
from .forms import WorkdayForm
from .models import Workday,User,Job,Workarea
from django.utils import timezone
import datetime
from django.utils.timezone import localtime

from django.views.generic.dates import TodayArchiveView,DayArchiveView



class ArticleTodayArchiveView(LoginRequiredMixin,DayArchiveView):
    queryset = User.objects.all()
    date_field = "date_created"
    allow_future = True
def day_beginning(dt=None):
    # if dt is None, localtime() operates on now()
    return localtime(dt).replace(hour=0, minute=0, second=0, microsecond=0)
def check_in_and_out_time(time):
    return (time - (day_beginning(None)+datetime.timedelta(hours=6)))>=datetime.timedelta(hours=10)
def homeview(request):
    current_time = timezone.now()
    if check_in_and_out_time(current_time):
        context = {'day_beginning':day_beginning()+datetime.timedelta(hours=6)}
    return render(request,"cutomuser/home.html",context)





class General_Create_View(CreateView):
    jobs=Job.objects.all()
    def post(self, request, *args, **kwargs):
      return super().post(request, *args, **kwargs)


class WorkareaView(DetailView):
    success_url = reverse_lazy('workarea')
    def get_object(self):
        return get_object_or_404(self.model,pk=self.kwargs.get('pk'))
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        workarea = self.get_object()
        context['members'] =workarea.members.all()
        context['jobs'] =Job.objects.all()
        return context



class General_Detail_View(DetailView):
    def get_object(self):
        return get_object_or_404(self.model,pk = self.kwargs.get('pk'))
  

    
class General_Update_View(UpdateView):
    pass

class General_List_View(LoginRequiredMixin,ListView):
    def get_queryset(self, **kwargs):
        return (self.model.objects.filter(date__lte = timezone.now())[:5])
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] =self.model.objects.filter(date__gte = (timezone.now()-datetime.timedelta(6))).first()
        return context
    

