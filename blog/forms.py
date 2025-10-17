from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['username', 'age', 'category', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'user-name',
                'placeholder': 'Введите имя'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'user-age',
                'placeholder': 'Введите возраст'
            }),
            'category': forms.Select(attrs={
                'class': 'user-category'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'user-password',
                'placeholder': 'Введите пароль'
            }),
        }