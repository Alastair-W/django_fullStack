from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addCourse', views.addCourse),
    path('requestDelete/<int:course_id>', views.requestDelete),
    path('postDelete/<int:course_id>', views.deleteCourse),
    path('editCourse/<int:course_id>', views.editCourse),
    path('postEdit/<int:course_id>', views.postEdit)
    
]