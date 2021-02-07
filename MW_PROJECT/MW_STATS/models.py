from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


# the Profile model is basically taking the User model and adding a field called gamertag
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    gamertag = models.CharField(max_length=30)


class Friends(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    gamertag1 = models.CharField(max_length=30, default='', blank=True)
    gamertag2 = models.CharField(max_length=30, default='', blank=True)
    gamertag3 = models.CharField(max_length=30, default='', blank=True)
    gamertag4 = models.CharField(max_length=30, default='', blank=True)
    gamertag5 = models.CharField(max_length=30, default='', blank=True)


class PrivateUsers(models.Model):
    name = models.CharField(max_length=10)
    all_time_score = models.IntegerField(default=0)


class Score(models.Model):
    name = models.ForeignKey(PrivateUsers, on_delete=CASCADE)
    first = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    third = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
