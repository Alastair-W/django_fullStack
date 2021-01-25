from django.shortcuts import render, redirect
from .models import User, Session, Message, Comment
import bcrypt
from django.contrib import messages
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def defineUser(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash
    )
    return redirect('/success')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    allMessages = reversed(Message.objects.all())
    displayUser = User.objects.get(id=request.session['user_id'])
    context = {
        'D': displayUser,
        'allM': allMessages,
    }
    return render(request, 'wall.html', context)

def checkLogin(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.loginVal(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    Session.objects.create(event="Log In", user=user)
    messages.success(request, "Logged In")
    return redirect('/success')

def loggedIn(request):
    if request.method == 'GET':
        return redirect('/')
    return redirect('/success')

def logout(request):
    userID = request.session['user_id']
    myUser = User.objects.get(id=userID)
    Session.objects.create(event="Log Out", user=myUser)
    request.session.clear()
    messages.success(request, "You have successfully logged out!")
    return redirect('/')

def profile(request):
    userID = request.session['user_id']
    return redirect(f'success/{ userID }')

def createMessage(request):
    if request.method == 'POST':
        userID = request.session['user_id']
        userObj = User.objects.get(id=userID)
        errors = Message.objects.messageVal(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
        Message.objects.create(
            message = request.POST['message'],
            user = userObj
        )
    return redirect('/success')

def createComment(request, message):
    if request.method == 'POST':
        relMessage = Message.objects.get(id=message)
        userID = request.session['user_id']
        userObj = User.objects.get(id=userID)
        errors = Comment.objects.commentVal(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
        Comment.objects.create(
            comment = request.POST['comment'],
            message = relMessage,
            user = userObj
        )
    return redirect('/success')
