# Generated by Django 3.1.4 on 2021-01-24 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug_tr',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title_tr',
        ),
    ]
