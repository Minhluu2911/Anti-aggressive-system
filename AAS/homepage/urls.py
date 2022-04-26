from django.urls import path

from . import views

app_name = 'homepage'
urlpatterns = [
    path('', views.home, name='home'),
    path('home/admin', views.home_admin, name='home_admin'),
]