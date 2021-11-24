from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pcell.models import company

# Create your models here.

class application(models.Model):
    name = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    applied_to = models.ManyToManyField(company,  blank=True)

    def __str__(self):
        return f'{self.name.username} Application'
