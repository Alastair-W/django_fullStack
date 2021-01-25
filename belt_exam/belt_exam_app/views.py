from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import User, Quote
from django.contrib import messages
import bcrypt

# Create your views here.
# GET
def index(request):
    return render(request, 'index.html')

def quotes(request):
    if request.session['user_id']:
        quotes = Quote.objects.all()
        likes = Quote.objects.aggregate(Sum('liked_by'))
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'q': quotes, 
            'l': likes,
            'user': user
        }
    return render(request, 'quotes.html', context)

def userPage(request, userID):
    userQ = Quote.objects.filter(added_by=User.objects.get(id=userID))
    userAddingQ = User.objects.get(id=userID)
    context = {
        'allQ': userQ,
        'user': userAddingQ
    }
    return render(request, 'userPage.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def profile(request):
    userInfo = User.objects.get(id=request.session['user_id'])
    context = {
        'user': userInfo
    }
    return render(request, 'editProfile.html', context)

# POST

def createUser(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validateReg(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash
    )
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/quotes')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validateLogin(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/quotes')

def addQuote(request):
    if request.method == 'GET':
        return redirect('/quotes')
    userID = request.session['user_id']
    userObj = User.objects.get(id=userID)
    errors = Quote.objects.quoteVal(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/quotes')
    Quote.objects.create(
        author = request.POST['author'],
        quote = request.POST['quote'],
        added_by = userObj
    )
    return redirect('/quotes')

def like(request, quote_id):
    userObj = User.objects.get(id=request.session['user_id'])
    quoteLiked = Quote.objects.get(id=quote_id)
    quoteLiked.liked_by.add(userObj)
    return redirect('/quotes')

def deleteQuote(request, quoteID):
    userID = request.session['user_id']
    quoteForDelete = Quote.objects.get(id=quoteID)
    quoteForDelete.delete()
    return redirect(f'/userPage/{userID}')

def makeEdits(request):
    if not request.session:
        return redirect('/')
    errors = Quote.objects.editVal(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/editProfile')
    userObj = User.objects.get(id=request.session['user_id'])
    userObj.first_name = request.POST['first_name']
    userObj.last_name = request.POST['last_name']
    userObj.email = request.POST['email']
    userObj.save()
    messages.success(request, "Your profile is updated") 
    return redirect('/editProfile')

    
