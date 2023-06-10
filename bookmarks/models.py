from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager

class User(AbstractUser):
    pass

class Bookmark(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    url = models.URLField()
    description = models.TextField(blank=True, max_length=2048)
    read_later = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)