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

from system.models import Store

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
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, default='/static/images/2.jpg', verbose_name='images')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    n_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    amount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=3)
    # variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    detail = RichTextField(max_length=255,blank=True)
    #tags = models.ManyToManyField(Tag)
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=status, default='', verbose_name="status")
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
        return reverse('detail', kwargs={'slug': self.slug})


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True, verbose_name='image')
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)

    def __str__(self):
        return self.product.title + " Img"


def get_unique_slug(sender, instance, **kwargs):
    num = 1
    slug = slugify(instance.title)
    unique_slug = slug
    while Product.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    instance.slug = unique_slug


pre_save.connect(get_unique_slug, sender=Product)



