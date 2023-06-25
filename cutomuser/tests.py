from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import User

# Create your tests here.
def create_user_with_perms(user_id):
    content_type = ContentType.objects.get_for_model(User)
    Permission.objects.create(
        content_type=content_type
        )
    user = User.objects.create(user_id=user_id)
    user_permisions = Permission.objects.filter(content_type = content_type)
    for perm in user_permisions:
       user.user_permissions.add(perm)
    return user


class MyUserModelTests(TestCase):
    def test_has_perm_with_a_string_in_user_permissions(self):
        """
        Should return true for the user has the permissions

        """
        user = create_user_with_perms("IDJDHJD")
        self.assertIs(user.has_perm("view_myuser"),True)
    
    def test_has_perm_with_a_user_without_any_perms(self):
        """
        Should return false

        """
        user = User.objects.create(user_id='user_id')
        self.assertIs(user.has_perm("view_myuser"),False)

    def test_has_perms_with_a_list_of_perms_with_a_user_with_perms(self):
        """ 
        Should return true if the user has the messioned perms
        """
        user = create_user_with_perms("IDJDHJD")
        self.assertIs(user.has_perm(["view_myuser","add_myuser"]),True)
    def test_has_perms_when_the_user_does_not_have_the_perms(self):
        """ 
        Should return False if the user doesn't have the messioned perms
        """
        user = create_user_with_perms("IDJDHJD")
        self.assertIs(user.has_perm(["view_muser","add_myuser"]),False)
    
    def test_has_perm_with_a_supperuser(self):

        """
        It should return true even when there are no perms assigned to the superuser
        So it can be tested with any perm

        """
        user = User.objects.create(user_id = "Coooljs")
        user.is_superuser = True
        self.assertIs(user.has_perm(["vier","add_myuser"]),True)







