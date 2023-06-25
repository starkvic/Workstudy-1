from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.urls import reverse,reverse_lazy
from .validators import validate_work_day,validate_phone


class UserManager(BaseUserManager):
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
        user.is_superuser = True
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
    ("",""),
    ('M','M'),
    ('F','F')
)

ROLES = (
    ("",""),
    ("Staff Member",'Staff Member'),
    ("Student Member",'Student Member'),
)

# Create your models here.
class User(PermissionsMixin,AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    user_id = models.CharField(max_length=150,primary_key=True)
    created = models.DateField(auto_now_add=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    gender = models.CharField(max_length=2,choices=GENDER,null=True)
    phone = models.CharField(max_length=10,validators=[validate_phone])
    first_name = models.CharField(max_length=200,null=False)
    middle_and_last_name = models.CharField(max_length=200,null=False)
    level = models.IntegerField(null=True)
    role = models.CharField(max_length=100,choices=ROLES,null=False,default="role")
    course = models.CharField(max_length=300,null=True)
    #last_name = models.CharField(max_length=200,null=True)

    class Meta:
        ordering = ["-created"]
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['user_id']

    def get_absolute_url(self):
        return reverse("user-detail", kwargs={"pk": self.user_id})
    
    def __str__(self):
        return self.email

    def is_in_group(self,group_name):
        return self.group.filter(name=group_name).exists()

    def has_perm(self, perms, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        if self.is_superuser and self.is_active:
            return True
        # return false if the list user permissions is none
        if [i.codename for i in self.user_permissions.all()]== []:
            return False
        #check if the perms value is a list of permissions or just a single string
        if type(perms)==type('str'):
            perms=[perms]
        
        for perm in perms:
            if perm not in [i.codename for i in self.user_permissions.all()]:
                return False
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
        return "{} {} {}".format(self.first_name,self.middle_and_last_name)

    
    @fullname.setter
    def fullname(self,name):
        self.first_name=self.middle_and_last_name=None
        try:
            self.first_name,self.middle_and_last_name = name.split(' ')
        except Exception as e:
            raise ValueError('You must provide at least two names')

class Job(models.Model):
     job_title = models.CharField(max_length=255)
     hourly_rate = models.IntegerField()
     created = models.DateTimeField(auto_now_add=True)
     archived = models.BooleanField(default=False,null=True)

     def __str__(self):
         return self.job_title
 #Student Schema

 #Applicaton schema
class Application(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     job = models.ForeignKey(Job,on_delete=models.CASCADE)
     created = models.DateTimeField(auto_now_add=True)
     is_approved = models.BooleanField(default=False)
     archived = models.BooleanField(default=False,null=True)

     class Meta:
        ordering = ["-created"]

     def __str__(self) -> str:
         return "{}  {}".format("Application",self.id)
     
class Workarea(models.Model):
    name = models.CharField(max_length=200)
    job = models.ForeignKey(Job,on_delete=models.SET_NULL,null=True)
    incharge = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    members = models.ManyToManyField(User,related_name="members",blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False,null=True)

    class Meta:
        ordering = ["-updated","-created"]

    def __str__(self):
        return self.name


 #Work days Schema
class Workday(models.Model):
     check_out = models.BooleanField(default=False)
     check_in = models.BooleanField(default=False)
     time_out= models.TimeField(auto_now_add=True)
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     workarea = models.ForeignKey(Workarea,on_delete=models.CASCADE)
     #created is the same as time in
     created = models.DateTimeField(auto_now_add=True,validators=[validate_work_day])

     class Meta:
        ordering = ["-time_out","-created"]
     def get_absolute_url(self):
         return reverse_lazy("workday-detail",kwargs={"pk":self.pk})
     
     def __str__(self):
         return "{}  /  {} hrs {}".format(str(self.date.day),str(self.date.year),str(self.date.hour))
    #  @property
    #  def time_in (self):
    #      if self.check_in:
    #          return self.current_time
    #  @property
    #  def time_out(self):
    #      if self.check_out:
    #          return self.current_time
         
    #  if check_in==True:
    #      check_out.editable = True
    #      check_in.editable=False
    #  if check_out==True:
    #      check_out.editable = False
    #      check_in.editable=True
             
    
         
     


