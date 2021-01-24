from django.shortcuts import render, redirect
from .models import User, Session
import bcrypt
from django.contrib import messages
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def defineUser(request):
    if request == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash
    )
    return redirect(f'success/{ newUser.id }')

def success(request, newUser):
    displayUser = User.objects.get(id=newUser)
    context = {
        'D': displayUser
    }
    return render(request, 'success.html', context)

def checkLogin(request):
    if request.method == 'POST':
        errors = User.objects.loginVal(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        Session.objects.create(event="Log In", user=user)
        messages.success(request, "You have successfully logged in!")
        return redirect(f'success/{ user.id }')

def logout(request):
    userID = request.session['user_id']
    myUser = User.objects.get(id=userID)
    Session.objects.create(event="Log Out", user=myUser)
    request.session.clear()
    messages.success(request, "You have successfully logged out!")
    return redirect('/')
