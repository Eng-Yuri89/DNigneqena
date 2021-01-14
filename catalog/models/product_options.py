from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from catalog.models.models import STATUS, Product, Image



class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    new_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Image.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Image.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


class Manufacturer(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    #store = models.ManyToManyField(Store, blank=True)
    image = models.IntegerField(blank=True, null=True, default=0)
    sort_order = models.IntegerField(default=0)
    slug = models.SlugField(null=title, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    # create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SingleProduct(models.Model):


    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # def getProductTags(self):
    # return self.tags.all()

    def __str__(self):
        return self.title
