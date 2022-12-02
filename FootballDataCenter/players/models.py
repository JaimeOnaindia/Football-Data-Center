from django.db import models

# Create your models here.


class BasePlayer(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey('geo.Country', on_delete=models.CASCADE, null=True)
    date_birth = models.DateField(null=True)
    team_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class BasePlayerFBREF(models.Model):
    GOALKEEPER = 'GK'
    CENTER_BACK = 'CB'
    RIGHT_BACK = 'RB'
    LEFT_BACK = 'LB'
    DEFENSIVE_MIDFIELDER = 'CMD'
    CENTRAL_MIDFIELDER = 'CM'
    ATTACKING_MIDFIELDER = 'CAM'
    RIGHT_WINGER = 'RW'
    LEFT_WINGER = 'LW'
    FORWARD = 'FW'
    UNKNOWN = 'UKW'

    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('CB', 'Center Back'),
        ('RB', 'Right Back'),
        ('LB', 'Left Back'),
        ('CMD', 'Defensive Midfielder'),
        ('CM', 'Central Midfielder'),
        ('CAM', 'Attacking Midfielder'),
        ('RW', 'Right Winger'),
        ('LW', 'Left Winger'),
        ('FW', 'Forward'),
        ('UKW', 'Unknown'),
    ]

    name = models.CharField(max_length=30)
    date_birth = models.DateField()
    team_name = models.CharField(max_length=30)
    original_position = models.CharField(max_length=3,
                                         choices=POSITION_CHOICES,
                                         default=UNKNOWN)
    matches_played = models.IntegerField()
