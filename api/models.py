"""Models for db and views"""
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
