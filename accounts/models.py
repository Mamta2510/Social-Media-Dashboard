from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    twitter_token = models.CharField(max_length=255, blank=True)
    facebook_token = models.CharField(max_length=255, blank=True)
    # Add other social tokens as needed

    def __str__(self):
        return self.user.username
