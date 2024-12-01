from django import forms

from .models import League
from users.models import CustomUser

class LeagueCreationForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'abbreviation', 'logo', 'password', 'members', 'moderators']
        widgets = {
            'password': forms.PasswordInput(),
        }