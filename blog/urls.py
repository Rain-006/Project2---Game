from django.urls import path
from . import views

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('create/', views.create_player, name='create_player'),
    path('edit/<int:pk>/', views.edit_player, name='edit_player'),
    path('delete/<int:pk>/', views.delete_player, name='delete_player'),
    path('login/', views.login_player, name='login'),
    path('logout/', views.logout_player, name='logout'),
    ]
