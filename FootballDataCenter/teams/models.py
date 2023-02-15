from django.db import models

# Create your models here.


class BaseTeam(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    team_name = models.CharField(max_length=30)
