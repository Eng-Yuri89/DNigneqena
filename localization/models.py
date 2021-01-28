from django.db import models

# Create your models here.
class Home(models.Model):
    title = models.CharField(max_length=10)
    content = models.CharField(max_length=300)
    slug = models.SlugField(max_length=30, unique=True)


    def __str__(self):
        return self.title

class Language(models.Model):
    name= models.CharField(max_length=20)
    code= models.CharField(max_length=5)
    image = models.ImageField(upload_to='images/lang/%Y/%m/%d', null=True, default='images/lang/en-gb.png')
    status=models.BooleanField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

