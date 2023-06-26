from django.urls import path,reverse,reverse_lazy
#for login and logout
from django.contrib.auth import views as auth_views
from . import views,models,forms

urlpatterns = [
    path("workarea/<pk>",views.WorkareaView.as_view(template_name='cutomuser/workarea.html',model=models.Workarea),name='workarea'),  # #Work day edit view - takes the check in time and check out time
    path("profile/<pk>",views.UserProfileView.as_view(template_name='cutomuser/profile.html',model=models.User),name="user-profile"),  # #Work day edit view - takes the check in time and check out time
    path('home/',views.HomeView.as_view(template_name='cutomuser/home.html',model=models.Workarea) , name='home'),
    path('logout/',auth_views.LogoutView.as_view(),name="logout"),
    path('login/',auth_views.LoginView.as_view(),name="login"),
    path('register/',views.General_Create_View.as_view(template_name="cutomuser/newuser.html",form_class=forms.UserCreationForm),name='register'),
    path('apply-for/<job_title>/',views.JobAppllicationView.as_view(template_name="cutomuser/job_application.html",form_class=forms.ApplicationForm),name='job_application'),
    

    # path(
    #     "<int:year>/<str:month>/<int:day>/",
    #     ArticleTodayArchiveView.as_view(),
    #     name="archive_day",
    # ),
    # path('work_day_detail/',General_List_View.as_view(model=Workday,template_name="cutomuser/workday.html"), name='workday-detail'),
    # path('workday/',General_Create_View.as_view(template_name="cutomuser/workday.html",form_class=WorkdayForm),name="workday"),
    # path('register/',General_Create_View.as_view(template_name="cutomuser/newuser.html",form_class=UserCreationForm),name='register'),
  
    
    # path('<str:pk>/',General_Detail_View.as_view(model=User), name='user-detail'),
    # path('workday/<int:pk>/',General_Detail_View.as_view(model=Workday), name='workday-detail'),
    # path('update_workday/<int:pk>/',General_Update_View.as_view(model=Workday,form_class=WorkdayForm,template_name="cutomuser/work_day_update.html"),name="workday_update")
]