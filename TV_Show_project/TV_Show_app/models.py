from django.db import models
from datetime import datetime

# Create your models here.

class TV_ShowManager(models.Manager):
    def show_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "'Title' must be at least 2 characters long"
        if TV_Show.objects.filter(title=postData['title']).exists():
            errors['title'] = "Title already exists" 
        if len(postData['network']) < 3:
            errors['network'] = "'Network' must be at least 3 characters long"
        x = len(postData['description'])
        if x > 0 and x < 10:
            errors['description'] = "Any description must be at least 10 characters long"
        if datetime.strptime(postData['relDate'], '%Y-%m-%d') > datetime.now():
            errors['relDate'] = "'Release Date' must be in the past" 
        return errors

class TV_Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    releaseDate = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = TV_ShowManager()

    def __repr__(self):
        return "TV Show Title: {}". format(self.title)

