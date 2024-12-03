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

class PokemonSearchForm(forms.Form):
    base_name__icontains = forms.CharField(label="Name Match", max_length=50, required=False)

    base_hp__gte = forms.IntegerField(label="Min HP", required=False)
    base_hp__lte = forms.IntegerField(label="Max HP", required=False)
    base_attack__gte = forms.IntegerField(label="Min Atk", required=False)
    base_attack__lte = forms.IntegerField(label="Max Atk", required=False)
    base_defense__gte = forms.IntegerField(label="Min Def", required=False)
    base_defense__lte = forms.IntegerField(label="Max Def", required=False)
    base_special_attack__gte = forms.IntegerField(label="Min SpA", required=False)
    base_special_attack__lte = forms.IntegerField(label="Max SpA", required=False)
    base_special_defense__gte = forms.IntegerField(label="Min SpD", required=False)
    base_special_defense__lte = forms.IntegerField(label="Max SpD", required=False)
    base_speed__gte = forms.IntegerField(label="Min Spd", required=False)
    base_speed__lte = forms.IntegerField(label="Max Spd", required=False)
    base_base_stat_total__gte = forms.IntegerField(label="Min BST", required=False)
    base_base_stat_total__lte = forms.IntegerField(label="Max BST", required=False)
    base_point_value__gte = forms.IntegerField(label="Min Pts", required=False)
    base_point_value__lte = forms.IntegerField(label="Max Pts", required=False)

    and_pokemon_types__type__name__iexact = forms.CharField(label="Types (AND)", max_length=150, required=False)
    or_pokemon_types__type__name__iexact = forms.CharField(label="Types (OR)", max_length=150, required=False)

    and_pokemon_abilities__name__iexact = forms.CharField(label="Abilities (AND)", max_length=150, required=False)
    or_pokemon_abilities__name__iexact = forms.CharField(label="Abilities (OR)", max_length=150, required=False)

    and_pokemon_moves__name__iexact = forms.CharField(label="Moves (AND)", max_length=150, required=False)
    or_pokemon_moves__name__iexact = forms.CharField(label="Moves (OR)", max_length=150, required=False)

    and_pokemon_coverage_moves__type__name__iexact = forms.CharField(label="Coverage Move Types (AND)", max_length=150, required=False)
    or_pokemon_coverage_moves__type__name = forms.CharField(label="Coverage Move Types (OR)", max_length=150, required=False)

    and_pokemon_special_moves__category__iexact = forms.CharField(label="Special Move Categories (AND)", max_length=150, required=False)
    or_pokemon_special_moves__category__iexact = forms.CharField(label="Special Move Categories (OR)", max_length=150, required=False)

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__lt___1 = forms.CharField(label="Resisted Types (AND)", max_length=150, required=False)
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__lt___1 = forms.CharField(label="Resisted Types (OR)", max_length=150, required=False)

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__gt___1 = forms.CharField(label="Weak Types (AND)", max_length=150, required=False)
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__gt___1 = forms.CharField(label="Weak Types (OR)", max_length=150, required=False)

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value___0 = forms.CharField(label="Immune Types (AND)", max_length=150, required=False)
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value___0 = forms.CharField(label="Immune Types (OR)", max_length=150, required=False)