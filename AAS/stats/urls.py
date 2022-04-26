from django.urls import path

from . import views

app_name = 'stats'
urlpatterns = [
    path('mystat/', views.mystat, name='mystat'),
    path('export_data/', views.export_data, name='export_data'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/admin/', views.leaderboard_admin, name='leaderboard_admin'),
]