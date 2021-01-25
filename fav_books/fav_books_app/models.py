from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')

# Create your models here.

class Validate(models.Manager):
    def registerVal(self, form):
        errors={}
        if len(form['first_name']) < 1:
            errors['first_name'] = "The first name field cannot be blank"
        if len(form['last_name']) < 1:
            errors['last_name'] = "The last name field cannot be blank"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Email not in a valid format"
        email_check = User.objects.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email is already in use"
        if form['password'] != form['confirm']:
            errors['password'] = "The passwords don't match"
        return errors

    def loginVal(self, form):
        errors={}
        check_user = User.objects.filter(email=form['email'])
        if not check_user:
            errors['email'] = "Invalid email/password"
            return errors
        else:
            check_pwd = bcrypt.checkpw(form['password'].encode(), check_user[0].password.encode())
            if not check_pwd:
                errors['password'] = 'Invalid email/password'
            return errors

    def bookVal(self, form):
        errors = {}
        if len(form['title']) < 1:
            errors['title'] = 'The title field cannot be empty'
        if len(form['description']) < 5:
            errors['description'] = 'The description field must be at least 5 characters long'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.TextField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validate()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=255)
    from_user = models.ForeignKey(User, related_name="book_upload", on_delete=models.CASCADE) 
    liked_by = models.ManyToManyField(User, related_name="liked_book")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validate()
