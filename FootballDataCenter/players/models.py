from django.db import models

# Create your models here.


class BasePlayer(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey('geo.Country', on_delete=models.CASCADE, null=True)
    date_birth = models.DateField(null=True)
    team_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class BasePlayerStatsFBREF(models.Model):
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
        ('DF', 'Center Back'),
        ('RB', 'Right Back'),
        ('LB', 'Left Back'),
        ('DF,MF', 'Defensive Midfielder'),
        ('MF', 'Central Midfielder'),
        ('CAM', 'Attacking Midfielder'),
        ('RW', 'Right Winger'),
        ('LW', 'Left Winger'),
        ('FW', 'Forward'),
        ('UKW', 'Unknown'),
    ]

    name = models.CharField(max_length=30)
    date_birth = models.DateField(null=True)
    team_name = models.CharField(max_length=30, null=True)
    original_position = models.CharField(max_length=10,
                                         choices=POSITION_CHOICES,
                                         default=UNKNOWN,
                                         null=True)
    matches_played = models.IntegerField(null=True)
    as_starter = models.IntegerField(null=True)
    minutes_played = models.IntegerField(null=True)
    goals = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    non_pen_goals = models.IntegerField(null=True)
    penalty_goals = models.IntegerField(null=True)
    penalty_attempts = models.IntegerField(null=True)
    yellow_cards = models.IntegerField(null=True)
    red_cards = models.IntegerField(null=True)
    exp_goals = models.FloatField(null=True)
    exp_non_pen_goals = models.FloatField(null=True)
    exp_goals_assists = models.FloatField(null=True)
    expected_non_pen_goals_assists = models.FloatField(null=True)
