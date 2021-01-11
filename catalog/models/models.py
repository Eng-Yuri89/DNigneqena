from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from DNigne import settings
from vendors.models import Store

STATUS = (
    ('True', 'Enable'),
    ('False', 'Disable'),
)


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})




def get_upload_path(instance, filename):
    model = instance.album.model.__class__._meta
    name = model.verbose_name_plural.replace(' ', '_')
    return f'{name}/images/{filename}'


def download_media_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(models.Model):
    status = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)  # many to one relation with Category
    #store = models.ForeignKey(Store, on_delete=models.CASCADE, null=False)  # many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, default='/static/images/2.jpg', verbose_name='images')
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, null=True)  # 100.00
    sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)  # 100.00
    discount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    amount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=3)
    # variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    detail = RichTextField(max_length=255,blank=True)
    #tags = models.ManyToManyField(Tag)
    slug = models.SlugField(null=False, unique=True)
    sale_active = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update_at']

    # def getProductTags(self):
    # return self.tags.all()

    def __str__(self):
        return self.title

    # method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        view_name = "products:detail_slug"
        return reverse(view_name, kwargs={"slug": self.slug})


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title
