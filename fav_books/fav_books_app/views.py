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
        allBooks = reversed(Book.objects.all())
        context = {
            "allBooks": allBooks,
            "this_user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def bookPage(request, bookID):
    context = {
        'this_book': Book.objects.get(id=bookID),
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'bookPage.html', context)

def editPage(request, bookID):
    context = {
        'edit_book': Book.objects.get(id=bookID)
    }
    return render(request, 'editBook.html', context)

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
    book = Book.objects.create(
        title = request.POST['title'],
        desc = request.POST['description'],
        from_user = curr_user
    )
    curr_user.liked_book.add(book)
    return redirect('/verifiedUser')

def favorite(request, bookID):
    curr_user = User.objects.get(id=request.session['user_id'])
    curr_book = Book.objects.get(id=bookID)
    if curr_user in curr_book.liked_by.all():
        curr_user.liked_book.remove(curr_book)
    else:
        curr_user.liked_book.add(curr_book)
    return redirect(f'/bookPage/{ bookID }')

def editBook(request, bookID):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.bookVal(request.POST)
    if errors:
        for error in errors:
            messages.error(request.errors[error])
        return redirect('/success')
    book = Book.objects.get(id=bookID)
    book.title = request.POST['title']
    book.desc = request.POST['description']
    book.save()
    return redirect(f'/editPage/{ bookID }')

