from django.db.models.signals import pre_save,post_save
from  .models import User, Workday,Application
from django.dispatch import receiver
from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType





# @receiver(post_save,sender=User)
# def give_permissions_post(sender,instance,created,**kwargs):
#     """ A student can edit the workday model, profile, can apply hence can add application can view a job"""
#     "Staff can edit his/her profile, can edit the workday model, can apply for a job and can supervise a group of other workers"
#     print(instance)
#     staffs = Group.objects.get(name="staff")
#     print(staffs.permissions.all())
#     if created and instance.role == "Staff Member":
#         # staffs.user_set.add(instance)
#         instance.groups.add(staffs)
#         instance.is_staff = True
#         #give staff perms or add to the staff group
#     elif instance.role == 'Student Member':
#         #get the model contenttypes for different models 
#         #give student perms / add into the student group
#         students = Group.objects.get(name="students")
#         students.user_set.add(instance)
#         instance.is_student = True



