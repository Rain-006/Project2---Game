from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['username', 'age', 'category', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }