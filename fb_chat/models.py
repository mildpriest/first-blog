from django.db import models
from django.utils import timezone


class ChatLog(models.Model):
    text = models.TextField()
    type = models.CharField(max_length=1, default='q')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

