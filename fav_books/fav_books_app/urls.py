from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registerPage', views.registerPage),
    path('registerUser', views.registerUser),
    path('login', views.logIn),
    path('verifiedUser', views.success),
    path('addBook', views.addBook),
    path('logout', views.logout)
]