from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=64)
    code_alpha_3 = models.CharField(max_length=5, primary_key=True)
    code_alpha_2 = models.CharField(max_length=3)
    region = models.CharField(max_length=16, null=True)
    sub_region = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f'{self.name} - {self.code_alpha_3}'
