from django.db import models
from django.utils import timezone
import datetime


class Request(models.Model):
    request = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    sender = models.CharField(max_length=64)
    responsible = models.CharField(max_length=64)
    in_progress = models.BooleanField()
    done = models.BooleanField()

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.request[:50]}..."
