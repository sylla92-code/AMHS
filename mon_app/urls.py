from django.contrib import admin
from django.urls import path
from .views import index_view, receive, envoie

urlpatterns = [
    path('mon_app/', index_view, name='index'),
    path('receive/', receive, name='receive'),
    path('envoie/', envoie, name='envoie'),
]
