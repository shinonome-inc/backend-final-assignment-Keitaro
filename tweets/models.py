from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

TWEET_MAX_LENGTH = 280


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=TWEET_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
