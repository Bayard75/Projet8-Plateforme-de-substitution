from django.db import models
from django.contrib.auth.models import User

from sub_website.models import Product
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255, default='')
    prenom = models.CharField(max_length=255, default='')
    profile_picture = models.ImageField(default='default.png', upload_to='profile_pic')
    favorites = models.ManyToManyField('sub_website.Product',
                                       related_name='users', blank=True)

    def __str__(self):
        return f'{self.user.username} Compte'
        