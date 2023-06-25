from django.urls import path,reverse,reverse_lazy
#for login and logout
from django.contrib.auth import views as auth_views
from . import views,models,forms
from .forms import WorkdayForm,UserCreationForm
from .models import User,Workday

urlpatterns = [
    path("workarea/<pk>",views.WorkareaView.as_view(template_name='cutomuser/workarea.html',model=models.Workarea)),
    # #Work day edit view - takes the check in time and check out time
    # path('home/',homeview , name='user-home'),
    # path(
    #     "<int:year>/<str:month>/<int:day>/",
    #     ArticleTodayArchiveView.as_view(),
    #     name="archive_day",
    # ),
    # path('work_day_detail/',General_List_View.as_view(model=Workday,template_name="cutomuser/workday.html"), name='workday-detail'),
    # path('workday/',General_Create_View.as_view(template_name="cutomuser/workday.html",form_class=WorkdayForm),name="workday"),
    # path('register/',General_Create_View.as_view(template_name="cutomuser/newuser.html",form_class=UserCreationForm),name='register'),
    # path('login/',auth_views.LoginView.as_view(template_name="cutomuser/login.html"),name="login"),
    # path('logout/',auth_views.LogoutView.as_view(template_name="cutomuser/logout.html"),name="logout"),
    # path('<str:pk>/',General_Detail_View.as_view(model=User), name='user-detail'),
    # path('workday/<int:pk>/',General_Detail_View.as_view(model=Workday), name='workday-detail'),
    # path('update_workday/<int:pk>/',General_Update_View.as_view(model=Workday,form_class=WorkdayForm,template_name="cutomuser/work_day_update.html"),name="workday_update")
]