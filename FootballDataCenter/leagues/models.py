from django.db import models

# Create your models here.


class LeaguesBase(models.Model):
    competition_name = models.CharField(max_length=64)
