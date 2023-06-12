from django.urls import path
#for login and logout
from django.contrib.auth import views as auth_views
from .views import General_Create_View,homeview,General_Detail_View
from .forms import WorkdayForm,UserCreationForm
from .models import MyUser

urlpatterns = [
    #Work day edit view - takes the check in time and check out time
    path('home/',homeview , name='user-home'),
    path('workday/',General_Create_View.as_view(template_name="cutomuser/workday.html",form_class=WorkdayForm)),
    path('register/',General_Create_View.as_view(template_name="cutomuser/newuser.html",form_class=UserCreationForm),name='register'),
    path('login/',auth_views.LoginView.as_view(template_name="cutomuser/login.html"),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name="cutomuser/logout.html"),name="logout"),
     path('<str:first_name>/',General_Detail_View.as_view(model=MyUser), name='user-detail'),
]