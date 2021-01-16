from django.shortcuts import render, redirect
from .models import TV_Show

# Create your views here.
def index(request):
    context = {
        'allShows': TV_Show.objects.all()
    }
    return render(request, 'index.html', context)

def addShow(request):
    return render(request, 'createShow.html')

def createTV(request):
    newShow = TV_Show.objects.create(
        title=request.POST['title'],
        network=request.POST['network'],
        releaseDate=request.POST['relDate'],
        description=request.POST['description']
    )
    return redirect(f'/viewShow/{ newShow.id }')

def viewShow(request, newShow):
    findShow = TV_Show.objects.get(id=newShow)
    context = {
        'show': findShow
    }
    return render(request, 'viewShow.html', context)

def editShow(request, show):
    findShow = TV_Show.objects.get(id=show)
    context = {
        'show': findShow
    }
    return render(request, 'editShow.html', context)

def makeEdits(request, show):
    updateShow = TV_Show.objects.get(id=show)
    updateShow.title = request.POST['title'],
    updateShow.network = request.POST['network'],
    updateShow.releaseDate = request.POST['relDate'],
    updateShow.description = request.POST['description']
    updateShow.save()
    return redirect(f'/viewShow/{ updateShow.id }')
