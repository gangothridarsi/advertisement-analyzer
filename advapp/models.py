from django.db import models
import os

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email_id = models.EmailField()
    password = models.CharField(max_length = 20)
    customer = models.BooleanField()
    
    def __str__(self):
        return self.username
    
class UserResults(models.Model):
    username = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    emotion_name = models.CharField(max_length=20)
    addId = models.ForeignKey('Advertisement', on_delete=models.SET_NULL, null=True)
    
def path_and_rename(instance, filename):
    upload_to = 'ads'
    ext = filename.split('.')[-1]
    if instance.addId:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        pass
    return os.path.join(upload_to, filename)

class Advertisement(models.Model):
    addId = models.CharField(max_length=30,primary_key = True)
    adDescription = models.CharField(max_length=600)
    adName = models.CharField(max_length=30)
    image = models.ImageField(upload_to = path_and_rename)
    username = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.addId)