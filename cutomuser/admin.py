
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm,UserCreationForm


from cutomuser.models import User,Job,Application,Workday,Workarea




class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "created", "is_admin","is_staff","user_id","middle_and_last_name"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
       # ("Personal info", {"fields": ["date_created"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email","user_id",'first_name', 'middle_and_last_name',"password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

    # Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class WorkdayAdmin(admin.ModelAdmin):
    list_display = ['created','check_out',"user"]
    pass
class JobAdmin(admin.ModelAdmin):
    list_display = ['id','job_title','hourly_rate']
    pass
admin.site.register(Workday,WorkdayAdmin)
admin.site.register(Job,JobAdmin)
admin.site.register([Application,Workarea])