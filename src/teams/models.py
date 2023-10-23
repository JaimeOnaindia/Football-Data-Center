from django.db import models

# Create your models here.


class BaseTeam(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey('geo.Country', on_delete=models.CASCADE, null=True)
    team_name = models.CharField(max_length=30)
