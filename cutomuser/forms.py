from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import User,Workday,Workarea,Application

class RegisterForm(forms.ModelForm):
    """
    The default 

    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )


    class Meta:
        model = User
        fields = ["user_id","email",'first_name','middle_and_last_name','gender','role','phone']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email",'first_name','middle_and_last_name','role','phone']


#Workday form 
class WorkdayForm(forms.ModelForm):
    class Meta:
        model=Workday
        fields = ["check_out","check_in","user"]

#Workarea form 
class WorkareaForm(forms.ModelForm):
    class Meta:
        model = Workarea
        fields = "__all__"
        exclude = ["archived"]
    def clean_incharge(self):
        incharge = self.cleaned_data.get('incharge')
        user = User.objects.filter(email = incharge)
        if user.exists():
            staff=User.objects.get(email=incharge)
            staff.is_staff = True
            staff.save()
        return incharge

#Application form
class ApplicationForm(forms.ModelForm):
   
    class Meta:
        model = Application
        fields = "__all__"
        exclude = ['archived']
    def clean_user(self):
        user= self.cleaned_data.get('user')
        user = Application.objects.filter(user=user)
        if user.exists():
            raise ValidationError(f"{user} has already applied for this job!")

