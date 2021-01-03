from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

from accounts.models import UserManager
from system.models import Store


class Vendor(AbstractBaseUser):
    """
    Description:This is going to be the main User Model
    """
    store = models.OneToOneField(Store, on_delete=models.PROTECT, null=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True )
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(blank=True, null=True,max_length=20)
    address = models.CharField(blank=True,null=True, max_length=150)
    city = models.CharField(blank=True,null=True, max_length=20)
    country = models.CharField(blank=True,null=True, max_length=50)
    image = models.ImageField(blank=True,null=True, upload_to='images/users/' ,default='images/dashboard/man.png')
    facebook = models.URLField(blank=True, max_length=50)
    instagram = models.URLField(blank=True, max_length=50)
    twitter = models.URLField(blank=True, max_length=50)
    youtube = models.URLField(blank=True, max_length=50)
    about = RichTextUploadingField(blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address or full name
        if self.first_name:
            return self.first_name
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        # Does the user have a specific permission?
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        return self.staff


    @property
    def is_active(self):
        "Is the user active?"
        return self.active
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

