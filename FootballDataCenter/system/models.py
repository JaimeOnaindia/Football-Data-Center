import datetime
import time

from django.db import models

# Create your models here.


class Process(models.Model):
    name = models.CharField(max_length=100)
    status_ok = models.BooleanField()
    start_time = models.DateTimeField(null=True)
    execution_time = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def start(self):
        self.start_time = datetime.datetime.now()

    def error_status(self):
        self.status_ok = False
        self.execution_time = time.time() - time.mktime(self.start_time.timetuple())
        self.save()

    def ok_status(self):
        self.status_ok = True
        self.execution_time = time.time() - time.mktime(self.start_time.timetuple())
        self.save()
