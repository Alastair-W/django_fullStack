from django.shortcuts import render, redirect
from .models import Course, Description
from django.contrib import messages
# Create your views here.
def index(request):
    context = {
    "allCourses": Course.objects.all()
    }
    return render(request, 'index.html', context)

def addCourse(request):
    errors = Course.objects.validate(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/')


    C = Course.objects.create(name = request.POST['name'])
    Description.objects.create(course=C, description = request.POST['description'])

    return redirect('/')

def requestDelete(request, course_id):
    forDeletion = Course.objects.get(id=course_id)
    context ={
        'D': forDeletion
    }
    return render(request, 'confirm.html', context)

def deleteCourse(request, course_id):
    forDeletion = Course.objects.get(id=course_id)
    forDeletion.delete()
    return redirect('/')


def editCourse(request, course_id):
    forEdit = Course.objects.get(id=course_id)
    context ={
        'Edit': forEdit
    }
    return render(request, 'edit.html', context)

def postEdit(request, course_id):
    errors = Course.objects.validate(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect(f'/editCourse/{ course_id }')
        
    forEdit = Course.objects.get(id=course_id)
    forEdit.name = request.POST['name']
    forEdit.description.description = request.POST['description']
    forEdit.save()
    forEdit.description.save()
    return redirect('/')