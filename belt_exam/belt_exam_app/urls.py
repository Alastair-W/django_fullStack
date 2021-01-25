from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.createUser),
    path('login', views.login),
    path('quotes', views.quotes),
    path('addQuote', views.addQuote),
    path('userPage/<int:userID>', views.userPage),
    path('logout', views.logout),
    path('likeQuote/<int:quote_id>', views.like),
    path('deleteQuote/<int:quoteID>', views.deleteQuote),
    path('editProfile', views.profile),
    path('makeEdits', views.makeEdits)
]