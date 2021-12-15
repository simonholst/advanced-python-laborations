from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models


class Route(models.Model):
    dep = models.CharField(max_length=200)
    dest = models.CharField(max_length=200)

    def __str__(self):
        return self.dep + '-' + self.dest
