# Generated by Django 3.1.4 on 2021-01-13 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20210113_2326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='multiImage',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
