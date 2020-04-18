from django.db import models

# Create your models here.

class Category(models.Model):

    name = models.CharField(primary_key = True, max_length = 256)

    def __str__(self):
        return self.name
    
class Product(models.Model):

    codebar = models.CharField(primary_key = True, max_length = 128)
    name = models.CharField(max_length = 256, unique=True)
    grade = models.CharField(max_length = 1)
    categories = models.ManyToManyField('Category',related_name='products')
    url = models.URLField()
    reperes = models.URLField()
    image = models.URLField()
    last_cat = models.CharField(max_length = 256)
    fallback_cat = models.CharField(max_length = 256, default='None')


    def __str__(self):
        return self.name
        