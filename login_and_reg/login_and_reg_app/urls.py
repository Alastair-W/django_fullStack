from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('defineUser', views.defineUser),
    path('success', views.success),
    path('checkLogin', views.checkLogin),
    path('logout', views.logout),
    path('profile', views.profile),
    path('loggedIn', views.loggedIn),
    path('postMessage', views.createMessage),
    path('postComment/<int:message>', views.createComment)
]