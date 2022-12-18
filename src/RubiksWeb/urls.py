#encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('', views.index),
    path('populate/', views.populateDB),
    path('loadRS/', views.loadRS),
    path('mostListenedArtists/', views.mostListenedArtists),
    path('mostFrequentTags/', views.mostFrequentTags),
    path('recommendedArtists/', views.recommendedArtists),
    path('admin/', admin.site.urls),
]