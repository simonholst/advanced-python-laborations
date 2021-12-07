from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Fruit(models.Model):
    name = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.name
