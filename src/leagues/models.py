from django.db import models

# Create your models here.


class BaseLeagueFBREF(models.Model):
    competition_name = models.CharField(max_length=64)
    matches_played = models.IntegerField()
    passes_attempted_per = models.FloatField()
    passes_live_per = models.FloatField()
    passes_dead_per = models.FloatField()
    free_kicks_passes_per = models.FloatField()
    key_passes_per = models.FloatField()
    through_balls_per = models.FloatField()
    crosses_per = models.FloatField()
    throws_in_per = models.FloatField()
    corner_kicks_per = models.FloatField()
    corner_kicks_in_per = models.FloatField()
    corner_kicks_out_per = models.FloatField()
    corner_kicks_straight_per = models.FloatField()
    passes_completed_per = models.FloatField()
    passes_offside_per = models.FloatField()
    passes_blocked_per = models.FloatField()
