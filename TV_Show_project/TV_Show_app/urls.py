from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addShow', views.addShow),
    path('createTV', views.createTV),
    path('viewShow/<int:newShow>', views.viewShow),
    path('editShow/<int:show>', views.editShow),
    path('makeEdits', views.makeEdits),
    path('deleteShow/<int:show>', views.deleteShow)
]