from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import validate_comma_separated_integer_list

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100, validators=[validate_comma_separated_integer_list])
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class Survey(models.Model):
    location = models.CharField(max_length = 100)
    region = models.CharField(max_length = 100)
    dateSampled = models.DateTimeField(default=timezone.now)
    transNumber = models.IntegerField()
    startLat = models.FloatField()
    startLong = models.FloatField()
    endLat = models.FloatField()
    endLong = models.FloatField()
    clams = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    rawData = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def str(self):
        return self.size