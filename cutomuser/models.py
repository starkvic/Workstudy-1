from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.urls import reverse
import datetime
from django.utils import timezone
from .validators import validate_work_day,validate_phone


class MyUserManager(BaseUserManager):
    def create_user(self, email,user_id, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            user_id=user_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,user_id,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            user_id,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    def create_staffuser(self,email,user_id,password=None):
        user = self.create_user(
            email,
            password=password,
            user_id=user_id
        )
        user.is_staff = True
        return user
GENDER = (
    ('M','M'),
    ('F','F')
)
# Create your models here.
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    user_id = models.CharField(max_length=150,primary_key=True)
    date_created = models.DateField(auto_now_add=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=2,choices=GENDER,null=True)
    phone = models.CharField(max_length=10,validators=[validate_phone])
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200,null=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['user_id']

    def get_absolute_url(self):
        return reverse("user-detail", kwargs={"user_id": self.user_id})
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
#LennoxEKK99
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_staff
    @property
    def fullname(self):
        if not self.middle_name:
            raise ValueError(f"User must have atleast two names")
        if self.last_name:
            return "{} {} {}".format(self.first_name,self.middle_name,self.last_name)
        else:
            return "{} {} {}".format(self.first_name,self.middle_name)

    
    @fullname.setter
    def fullname(self,name):
        self.first_name=self.middle_name=self.last_name=None
        try:
            if len(name.split(' ')) == 3:
                self.first_name,self.middle_name,self.last_name = name.split(' ')
            else:
                self.first_name,self.middle_name = name.split(' ')
        except Exception as e:
            print(e)


        
# {e} 


 # class Admin(MyUser):
 #     admin_id = models.CharField(max_length = 255,primary_key=True)
 # Jobs Schema
class Job(models.Model):
     job_id = models.CharField(max_length=255,primary_key=True)
     job_title = models.CharField(max_length=255)
     hourly_rate = models.IntegerField()
     staff_or_admin_id = models.ForeignKey(MyUser,on_delete=models.CASCADE)
     date_time_created = models.DateTimeField(auto_now_add=True)
 #Student Schema
class Student(MyUser):
     level = models.IntegerField()
     course = models.CharField(max_length=300)
    # password = models.CharField(max_length=40)
   
 #staff schema
 # class Staff(MyUser):
 #     staff_id = models.CharField(max_length = 255,primary_key=True)
 #Applicaton schema
class Application(models.Model):
     user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE)
     job_id = models.ForeignKey(Job,on_delete=models.CASCADE)
     date_time_applied = models.DateTimeField(auto_now_add=True)
     is_approved = models.BooleanField(default=True)
 #Work days Schema
class Workday(models.Model):
     current_time = models.TimeField(auto_now_add=True)
    # time_out = models.TimeField(auto_now_add=True)
     check_out = models.BooleanField(default=False)
     check_in = models.BooleanField(default=False)
     #check_out.editable=False
     user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE)
     #job_id = models.ForeignKey(Job,on_delete=models.CASCADE)
     date = models.DateField(auto_now_add=True,validators=[validate_work_day])

     @property
     def time_in (self):
         if self.check_in:
             return self.current_time
     @property
     def time_out(self):
         if self.check_out:
             return self.current_time
         
     if check_in==True:
         check_out.editable = True
         check_in.editable=False
     if check_out==True:
         check_out.editable = False
         check_in.editable=True
             
    
         
     


