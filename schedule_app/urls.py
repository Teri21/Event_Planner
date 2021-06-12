from django.urls import path, include
from. import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('welcome', views.welcome),
    path('logout', views.logout),
    path('create_event', views.create_event),
    path('one_event/<int:id>', views.one_event),
    path('edit/<int:id>', views.edit),
    path('add_like/<int:id>', views.add_like),
    path('delete_event/<int:id>', views.delete_event),

]
