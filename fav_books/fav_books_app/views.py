from django.shortcuts import render, redirect
from .models import User, Book
import bcrypt
from django.contrib import messages

# Create your views here.

#GET
def index(request):
    return render(request, 'index.html')

def registerPage(request):
    return render(request, 'register.html')

def success(request):
    if request.session['user_id']:
        allBooks = Book.objects.all()
        context = {
            "allBooks": allBooks
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('/')

def logout(request):
    userID = request.session['user_id']
    myUser = User.objects.get(id=userID)
    request.session.clear()
    return redirect('/')

#POST

def registerUser(request):
    if request.method == 'GET':
        return redirect('/registerPage')
    errors = User.objects.registerVal(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/registerPage')
    pwd = request.POST['password']
    hashpwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashpwd
    )
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/verifiedUser')

def logIn(request):
    if request.method == 'GET':
        return redirect('/registerPage')
    errors = User.objects.loginVal(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/registerPage')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/verifiedUser')

def addBook(request):
    if request.method == 'GET':
        return redirect('/success')
    errors = User.objects.bookVal(request.POST)
    if errors:
        for error in errors:
            messages.error(request.errors[error])
        return redirect('/success')
    curr_user = User.objects.get(id=request.session['user_id'])
    Book.objects.create(
        title = request.POST['title'],
        desc = request.POST['description'],
        from_user = curr_user
    )
    return redirect('/verifiedUser')
