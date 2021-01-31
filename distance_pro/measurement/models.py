from django.db import models

# Create your models here.

class  Measurement(models.Model):
    location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.CharField(max_length=100)
    created = models.DateTimeField(max_length=100, auto_now_add=True)

    def __str__(self):
        return f'Distance from {self.location} to {self.destination} is {self.distance}'