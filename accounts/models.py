from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField()
    followee = models.ManyToManyField("self", related_name="follower", symmetrical=False, blank=True)


# class FriendShip(models.Model):
