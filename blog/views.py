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

# Редактировать игрока
def edit_player(request, pk):
    player = get_object_or_404(Player, pk=pk)
    message = ''
    player_id = request.session.get('player_id')
    if not player_id:
        return redirect('login')
    # Проверка, принадлежит ли редактируемый профиль текущему пользователю
    if request.session['player_id'] != player.id:
        message = 'У вас нет прав для редактирования этого профиля'
        return render(request, 'blog/edit_player.html', {'player': player, 'message': message})
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'blog/edit_player.html', {'form': form, 'player': player, 'message': message})