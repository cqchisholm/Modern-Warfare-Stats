from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


# the Profile model is basically taking the User model and adding a field called gamertag
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    gamertag = models.CharField(max_length=30)
