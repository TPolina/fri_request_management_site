from django.db import models
from django.utils import timezone
from model_utils.fields import StatusField
from model_utils import Choices
import datetime


class User(models.Model):
    user_id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, null=True)
    user_name = models.CharField(max_length=64, null=True)

    def __str__(self):
        if self.last_name is not None:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.first_name}'


class Message(models.Model):
    STATUS = Choices('to do', 'in progress', "done")

    update_id = models.IntegerField(unique=True, primary_key=True)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    responsible = models.CharField(max_length=64)
    status = StatusField()

    def __str__(self):
        return f'{self.message[:50]}...'
