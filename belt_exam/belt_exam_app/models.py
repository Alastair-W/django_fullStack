from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')

# Create your models here.
class Validate(models.Manager):
    def validateReg(self, form):
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

    def validateLogin(self, form):
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

    def quoteVal(self, form):
        errors={}
        if len(form['author']) < 3:
            errors['author'] = "Author field needs to be more than 3 characters long!"
        if len(form['quote']) < 10:
            errors['quote'] = "Quote field needs to be more than 10 characters long!"
        return errors
    
    def editVal(self, form):
        errors={}
        if len(form['first_name']) < 2:
            errors['first_name'] = "First Name needs to be more than two characters"
        if len(form['last_name']) < 2:
            errors['last_name'] = "Last Name needs to be more than two characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Email not in a valid format" 
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validate()

class Quote(models.Model):
    author = models.CharField(max_length=50)
    quote = models.TextField(max_length=255)
    added_by = models.ForeignKey(User, related_name="quote_added", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_quotes')
    objects = Validate()