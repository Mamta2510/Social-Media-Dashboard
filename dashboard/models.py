from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_id = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    created_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username} - {self.text[:50]}"
