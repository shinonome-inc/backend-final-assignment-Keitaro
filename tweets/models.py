from django.db import models

from accounts.models import User

TWEET_MAX_LENGTH = 280


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=TWEET_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
