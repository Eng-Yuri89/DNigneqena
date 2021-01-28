from django.db import models

# Create your models here.


from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.models import User
from localization.models import Language


class Setting(models.Model):
    STATUS = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )
    phone = models.IntegerField(blank=True,   default='510')
    email = models.EmailField(blank=True, max_length=50 , default='', null=True)
    image = models.ImageField(upload_to='images/store/',   default='images/store/nigne.png')
    facebook = models.URLField(blank=True, max_length=50 , default='', null=True)
    instagram = models.URLField(blank=True, max_length=50 , default='', null=True)
    twitter = models.URLField(blank=True, max_length=50 , default='', null=True)
    youtube = models.URLField(blank=True, max_length=50 , default='', null=True)
    status = models.CharField(max_length=10, choices=STATUS , default='Enable')
    create_at = models.DateTimeField(auto_now=True ,null=False)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email



        ## method to create a fake table field in read only mode

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

llist = Language.objects.filter(status=True)
list1 = []
for rs in llist:
    list1.append((rs.code,rs.name))
langlist = (list1)


class SettingLang(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE) #many to one relation with Category
    lang =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150 , null=True ,default='Nigne')
    keywords = models.CharField(max_length=255, default=' ', null=True)
    company = models.CharField(max_length=50, default=' ', null=True)
    address = models.CharField(blank=True, max_length=100, default=' ', null=True)
    about = RichTextUploadingField(blank=True, default='', null=True)
    contact = RichTextUploadingField(blank=True, default='', null=True)
    slug = models.SlugField(null=False)
    def __str__(self):
        return self.setting



class Images(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/store/')

    def __str__(self):
        return self.title


