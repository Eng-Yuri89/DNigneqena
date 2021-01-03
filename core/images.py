import datetime
import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.crypto import get_random_string

from DNigne import settings

def get_upload_path(instance, filename):
    model = instance.album.model.__class__._meta
    name = model.verbose_name_plural.replace(' ', '_')
    return f'{name}/images/{filename}'

def saved_thumb_path(instance, filename):
    model = instance.album.model.__class__._meta
    name = model.verbose_name_plural.replace(' ', '_')
    return f'{name}/images/thumb/{filename}'

class Photo(models.Model):
    photo = models.ImageField(upload_to=get_upload_path)
    photo_compressed = models.ImageField(upload_to=saved_thumb_path, editable=False)
    thumbnail = models.ImageField(upload_to=saved_thumb_path, editable=False)

    def save(self, *args, **kwargs):

        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        if not self.make_thumbnail(small=True):
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Photo, self).save(*args, **kwargs)

    def make_thumbnail(self, small=False):
        return make_thumbnail(self, small)

def saved_directory_path(instance, filename, root):
    now_time = datetime.now()
    current_day = now_time.day
    current_month = now_time.month
    current_year = now_time.year
    return '{root}/{year}/{month}/{day}/{user}/{random}/{filename}'.format(root=root,
                                                                           year=current_year,
                                                                           month=current_month,
                                                                           day=current_day,
                                                                           user=instance.user.username,
                                                                           random=get_random_string(),
                                                                           filename=filename, )


def saved_image_path(instance, filename):
    return saved_directory_path(instance, filename, 'profile/images')


def saved_thumb_path(instance, filename):
    return saved_directory_path(instance, filename, 'profile/thumbs')

def make_thumbnail(self, small=False):
    thumb_name, thumb_extension = os.path.splitext(self.photo.name)
    thumb_extension = thumb_extension.lower()

    image = Image.open(self.photo)

    if small:
        image.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)
        thumb_filename = thumb_name + '_thumb' + thumb_extension

    else:
        image.thumbnail((700, 700), Image.ANTIALIAS)
        thumb_filename = thumb_name + '_compressed' + thumb_extension

    if thumb_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif thumb_extension == '.gif':
        FTYPE = 'GIF'
    elif thumb_extension == '.png':
        FTYPE = 'PNG'
    else:
        return False  # Unrecognized file type

    # Save thumbnail to in-memory file as StringIO
    temp_thumb = BytesIO()
    image.save(temp_thumb, FTYPE, quality=70)
    temp_thumb.seek(0)

    if small:
        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    else:
        self.photo_compressed.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    temp_thumb.close()

    return True