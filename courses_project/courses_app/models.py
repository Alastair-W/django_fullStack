from django.db import models

# Create your models here.
class CourseManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['name']) < 5:
            errors['name'] = "Course name needs to be more than 5 characters"
        if len(form['description']) < 15:
            errors['description'] = "Course description needs to be more than 15 characters"    
        return errors

class Course(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CourseManager()

class Description(models.Model):
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CourseManager()