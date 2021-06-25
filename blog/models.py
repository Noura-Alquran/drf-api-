from django.contrib.auth import get_user_model
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=64)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField()

