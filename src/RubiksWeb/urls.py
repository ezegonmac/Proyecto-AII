# encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', views.home),
    path('', views.home),
    path('home/', views.home, name='home'),
    path('scraping/', views.scraping, name='scraping'),
    path('search_all/', views.search_all, name='search_all'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:id>', views.product_detail, name='product'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('like/', views.like, name='like'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
