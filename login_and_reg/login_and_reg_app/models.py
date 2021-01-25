from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')

# Create your models here.
class Validate(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = "First Name needs to be more than two characters"
        if len(form['last_name']) < 2:
            errors['last_name'] = "Last Name needs to be more than two characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Email not in a valid format" 
        email_check = User.objects.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email is already in use"
        if form['password'] != form['confirm']:
            errors['password'] = "Your passwords don't match"
        return errors

    def loginVal(self, form):
        errors={}
        check_user = User.objects.filter(email=form['email'])
        if not check_user:
            errors['email'] = 'Invalid email/password'
            return errors
        else:
            pwd = form['password']
            check_pwd = bcrypt.checkpw(pwd.encode(), check_user[0].password.encode())
            if not check_pwd:
                errors['password'] = 'Invalid email/password'
        return errors  

    def messageVal(self, form):
        errors = {}
        if len(form['message']) < 1:
            errors['message'] = "Message field is empty!"
        return errors

    def commentVal(self, form):
        errors={}
        if len(form['comment']) < 1:
            errors['comment'] = "Comment field is empty"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validate()

class Session(models.Model):
    event = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name="session", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="message", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validate()

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    message = models.ForeignKey(Message, related_name="comment", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="comment", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validate()