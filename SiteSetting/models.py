from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.models import User


class Store(models.Model):
    STATUS = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )
    vendor = models.ForeignKey(User ,  on_delete=models.CASCADE)
    title = models.CharField(max_length=150 , null=True ,default='Nigne')
    keywords = models.CharField(max_length=255 , default=' ' , null=True)
    company = models.CharField(max_length=50 , default=' ', null=True)
    address = models.CharField(blank=True, max_length=100 , default=' ', null=True)
    phone = models.IntegerField(blank=True,   default='510')
    email = models.EmailField(blank=True, max_length=50 , default='', null=True)
    #smtp_server = models.CharField(blank=True, max_length=50 , default='g', null=True)
    #smtp_email = models.CharField(blank=True, max_length=50 , default='g', null=True)
    #smtp_password = models.CharField(blank=True, max_length=10 , default='g', null=True)
    #smtp_port = models.CharField(blank=True, max_length=5 , default='g', null=True)
    image = models.ImageField(upload_to='images/store/',   default='images/store/nigne.png')
    icon = models.ImageField(blank=True, upload_to='images/store/icon/', null=True)
    facebook = models.URLField(blank=True, max_length=50 , default='', null=True)
    instagram = models.URLField(blank=True, max_length=50 , default='', null=True)
    twitter = models.URLField(blank=True, max_length=50 , default='', null=True)
    youtube = models.URLField(blank=True, max_length=50 , default='', null=True)
    about = RichTextUploadingField(blank=True , default='', null=True)
    contact = RichTextUploadingField(blank=True , default='', null=True)
    #references = RichTextUploadingField(blank=True , default='', null=True)
    status = models.CharField(max_length=10, choices=STATUS , default='Enable')
    slug = models.SlugField(null=False)
    create_at = models.DateTimeField(auto_now=True ,null=False)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



        ## method to create a fake table field in read only mode

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""



class Images(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/store/')

    def __str__(self):
        return self.title