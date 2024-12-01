from django import forms

from .models import League
from users.models import CustomUser

class LeagueCreationForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'logo', 'password', 'members', 'moderators']
        widgets = {
            'password': forms.PasswordInput(),
        }