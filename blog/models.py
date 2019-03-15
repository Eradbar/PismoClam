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
    surveyName = models.CharField(max_length = 200)
    location = models.CharField(max_length = 200)
    region = models.CharField(max_length = 100)
    dateSampled = models.DateTimeField(default=timezone.now)
    transNumber = models.IntegerField()
    startTime = models.CharField(max_length = 50)
    endTime = models.CharField(max_length = 50)
    lowTideTime = models.CharField(max_length = 50)
    startLat = models.FloatField()
    startLong = models.FloatField()
    endLat = models.FloatField()
    endLong = models.FloatField()
    lowTide = models.CharField(max_length = 50)
    clams = models.TextField()
    waterTemp = models.CharField(max_length = 100)
    airTemp = models.CharField(max_length = 100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def str(self):
        return self.surveyName
    
    def get_absolute_url(self):
        return reverse('survey-detail', kwargs={'pk': self.pk})