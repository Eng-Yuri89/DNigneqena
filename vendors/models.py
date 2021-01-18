from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import AbstractBaseUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.models import User, UserManager


class Store(models.Model):
    STATUS = (
        ('Enable', 'Enable'),
        ('Disable', 'Disable'),
    )

    vendor = models.OneToOneField(to=User , on_delete=models.CASCADE ,blank=True )
    #catalog = models.ForeignKey(Product,on_delete=models.CASCADE ,null=True , blank=True)
    title = models.CharField(max_length=150 , null=True ,default='Nigne')
    keywords = models.CharField(max_length=255 , default=' ' , null=True)
    company = models.CharField(max_length=50 , default=' ', null=True)
    address = models.CharField(blank=True, max_length=100 , default=' ', null=True)
    phone = models.IntegerField(blank=True,   default='510')
    email = models.EmailField(blank=True, max_length=50 , default='', null=True , unique=True)
    image = models.ImageField(upload_to='images/store/',   default='images/store/nigne.png')
    facebook = models.URLField(blank=True, max_length=50 , default='', null=True)
    instagram = models.URLField(blank=True, max_length=50 , default='', null=True)
    twitter = models.URLField(blank=True, max_length=50 , default='', null=True)
    youtube = models.URLField(blank=True, max_length=50 , default='', null=True)
    about = RichTextUploadingField(blank=True , default='', null=True)
    contact = RichTextUploadingField(blank=True , default='', null=True)
    status = models.CharField(max_length=10, choices=STATUS , default='Disable')
    slug = models.SlugField(null=False)
    create_at = models.DateTimeField(auto_now=True ,null=False)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.title



        ## method to create a fake table field in read only mode

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        view_name = "store:detail_slug"
        return reverse(view_name, kwargs={"slug": self.slug})











