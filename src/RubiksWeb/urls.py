# encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views
from django.urls import include

urlpatterns = [
    path('', views.index),
    path('populate/', views.populateDB),
    path('loadRS/', views.loadRS),
    path('mostListenedArtists/', views.mostListenedArtists),
    path('mostFrequentTags/', views.mostFrequentTags),
    path('recommendedArtists/', views.recommendedArtists),
    path('admin/', admin.site.urls),
    path('styles/', views.styles),
    path('home/', views.home, name='home'),
    path('scraping/', views.scraping, name='scraping'),
    path('search_all/', views.search_all, name='search_all'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:id>', views.product_detail, name='product'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('like/', views.like, name='like'),
]
