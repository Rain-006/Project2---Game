from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Player
from .forms import PlayerForm
import random
from django.contrib import messages

# Список всех пользователей
def player_list(request):
    players = Player.objects.all()
    return render(request, 'blog/player_list.html', {'players': players})

# Создание нового пользователя
def create_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm()
    return render(request, 'blog/create_player.html', {'form': form})