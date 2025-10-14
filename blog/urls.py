from django.urls import path
from . import views

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('create/', views.create_player, name='create_player'),
    ]
