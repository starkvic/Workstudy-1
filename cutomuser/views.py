from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.views.generic import (
    CreateView,DetailView
)
from .forms import WorkdayForm
from .models import Workday

def homeview(request):
    return render(request,"cutomuser/home.html")

class General_Create_View(CreateView):
    def form_valid(self, form):
        return super().form_valid(form)

class General_Detail_View(DetailView):
    def get_object(self):
        return get_object_or_404(self.model,user_id = self.kwargs.get('user_id'))

