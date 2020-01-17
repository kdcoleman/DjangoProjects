import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    join_date = models.DateTimeField('date joined')
    email_confirmed = models.BooleanField(default=False)

    def joined_recently(self):
        return timezone.now() - datetime.timedelta(days=7) <= self.join_date <= timezone.now()

    def __str__(self):
        first = self.first_name
        last = self.last_name
        full = first + " " + last
        return full
