from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=64)
    code_alpha_3 = models.CharField(max_length=5)
    code_alpha_2 = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.name} - {self.code_alpha_3}'
