# Generated by Django 3.1.4 on 2021-01-15 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20210115_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banners',
            name='image_w',
        ),
        migrations.AddField(
            model_name='bannergroup',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bannergroup',
            name='owner',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='banners',
            name='caption',
            field=models.CharField(default='Nigne', max_length=150, null=True, verbose_name='Title'),
        ),
    ]