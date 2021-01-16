from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from accounts.models import User

import os

from PIL import Image
from io import BytesIO

from django.core.files import File
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import ugettext_lazy as _


class SizedImageFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        tmp = BytesIO()
        root, ext = os.path.splitext(content.name)
        image = Image.open(content.file)
        image.thumbnail((self.field.width, self.field.height), Image.ANTIALIAS)
        image.save(tmp, Image.EXTENSION[ext])
        tmp.seek(0)
        super(SizedImageFieldFile, self).save(name, File(tmp), save)


class SizedImageField(ImageField):
    attr_class = SizedImageFieldFile

    def __init__(self, verbose_name=None, width=None, height=None, **kwargs):
        if width is None or height is None:
            raise ValueError('width and height are required for SizedImageField.')
        self.width = width
        self.height = height
        kwargs.setdefault(
            'help_text',
            _('The picture will be resized to fit {width}px x {height}px.').format(
                width=width, height=height
            )
        )
        super(SizedImageField, self).__init__(verbose_name=verbose_name, **kwargs)


class BannerGroup(models.Model):
    STATUS = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )

    banner_name = models.CharField(max_length=150, null=True, default='Nigne')
    status = models.CharField(max_length=10, choices=STATUS, default='Enable')

    def __str__(self):
        return str(self.id)


class Banners(models.Model):
    banner = models.ForeignKey(BannerGroup,
                               related_name="banner_group", on_delete=models.CASCADE)
    caption = models.CharField(max_length=150, null=True, default='Nigne', verbose_name="Title")
    link = models.URLField(null=True, blank=True)
    image = ProcessedImageField(upload_to='avatars',
                                processors=[ResizeToFill(1920, 718)],
                                format='JPEG',
                                options={'quality': 60})
    sort_order = models.SmallIntegerField(default=0, blank=True, null=False)

    def __str__(self):
        return self.caption

        ## method to create a fake table field in read only mode

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
