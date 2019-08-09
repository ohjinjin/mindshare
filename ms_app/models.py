from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# ohjinjin, 08/02/19 AM 10:45 defined profile class

class Profile1(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)  #id,pw,email, firstname, lastname
    evidence = models.ImageField(upload_to = 'images/')  # 추가 chanho - 19_8_2_11:43
    sex = models.CharField(max_length=15, blank=True)
    birth_date = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15,blank=True)
    agreement1 = models.CharField(max_length=10, blank=True)
    agreement2 = models.CharField(max_length=10, blank=True)
    agreement3 = models.CharField(max_length=10, blank=True)

"""
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()"""

class Wish_Book(models.Model):
    state = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher =models.CharField(max_length=200)
    pub_date = models.CharField(max_length=200)


# Library model 수정 8_8 찬호   

class Library(models.Model):# ohjinjin 080619 PM15:08
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher =models.CharField(max_length=200)
    record = models.FileField(upload_to = 'musics/',blank=True)
    Bookperm = models.BooleanField(default=False)
    pub_date = models.CharField(max_length=200) # 추가
    """
class Library(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher =models.CharField(max_length=200)
    pub_date = models.CharField(max_length=200)
    record = models.FileField(upload_to = 'musics/',blank=True)
"""