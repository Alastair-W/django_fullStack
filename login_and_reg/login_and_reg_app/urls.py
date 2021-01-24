from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('defineUser', views.defineUser),
    path('success/<int:newUser>', views.success),
    path('checkLogin', views.checkLogin),
    path('logout', views.logout)
]