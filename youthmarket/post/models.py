from statistics import mode
from django.db import models

class Icon(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, null=True, upload_to='icons')
    def __str__(self):
        return self.title
