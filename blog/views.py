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

# Удалить игрока
def delete_player(request, pk):
    player = get_object_or_404(Player, pk=pk)
    message = ''
    player_id = request.session.get('player_id')
    if not player_id:
        return redirect('login')
    # Проверка, авторизован ли пользователь
    if 'player_id' not in request.session:
        return redirect('login_player')
    # Проверка, принадлежит ли редактируемый профиль текущему пользователю
    if request.session['player_id'] != player.id:
        message = 'У вас нет прав для редактирования этого профиля'
    if request.method == 'POST':
        player.delete()
        return redirect('player_list')

    return render(request, 'blog/delete_player.html', {'player': player,  'message': message})

# Авторизация
def login_player(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            player = Player.objects.get(username=username, password=password)
            request.session['player_id'] = player.id
            return redirect('game')
        except Player.DoesNotExist:
            message = 'Неверное имя пользователя или пароль'
    return render(request, 'blog/login.html', {'message': message})

# Выход
def logout_player(request):
    request.session.flush()
    return redirect('login')

# Игра
def game(request):
    player_id = request.session.get('player_id')
    if not player_id:
        return redirect('login')
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'blog/index.html', {'player': player})

# API для обновления статистики
def api_play(request):
    player_id = request.session.get('player_id')
    if not player_id:
        return JsonResponse({'error': 'not_logged_in'})
    player = Player.objects.get(id=player_id)

    move = request.GET.get('move')
    options = ['Rock', 'Paper', 'Scissors']
    computer = random.choice(options)

    if move == computer:
        result = 'Tie'
    elif (move == 'Rock' and computer == 'Scissors') or \
         (move == 'Paper' and computer == 'Rock') or \
         (move == 'Scissors' and computer == 'Paper'):
        result = 'win'
    else:
        result = 'loss'

    # 👇 добавлено — начисление звёзд и подсчёт статистики
    if result == 'win':
        player.add_win()  # ✅ 4 пробела перед этой строкой
    elif result == 'loss':
        player.losses += 1
        player.save()
    else:
        player.ties += 1
        player.save()
    # 👆 конец добавленного

    return JsonResponse({
        'computer': computer,
        'result': result,
        'wins': player.wins,
        'losses': player.losses,
        'ties': player.ties,
        'stars': getattr(player, 'stars', 0)
    })
