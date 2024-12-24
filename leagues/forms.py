from django import forms

from .models import Team
from pokemons.models import SpecialMoveCategory, Type, PokemonAbility, PokemonMove

TYPE_CHOICES = [(t.name.capitalize(), t.name.capitalize()) for t in Type.objects.all().order_by('name')]
ABILITY_CHOICES = [(x['name'].capitalize(), x['name'].capitalize()) for x in PokemonAbility.objects.values('name').distinct().order_by('name')]
MOVE_CHOICES = [(x['name'].capitalize(), x['name'].capitalize()) for x in PokemonMove.objects.values('name').distinct().order_by('name')]

class LeagueJoinForm(forms.Form):
    league_name = forms.CharField(label="League Name", max_length=50)
    league_password = forms.CharField(label="League Password", max_length=20)
    team_name = forms.CharField(label="Team Name", max_length=50)

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'logo']

class DataUploadForm(forms.Form):
    file = forms.FileField()

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

    and_pokemon_types__type__name__iexact = forms.MultipleChoiceField(
        label="Types (AND)",
        choices=TYPE_CHOICES,
        required=False
    )
    or_pokemon_types__type__name__iexact = forms.MultipleChoiceField(
        label="Types (OR)",
        choices=TYPE_CHOICES,
        required=False
    )

    and_pokemon_abilities__name__iexact = forms.MultipleChoiceField(
        label="Abilities (AND)",
        choices=ABILITY_CHOICES,
        required=False
    )
    or_pokemon_abilities__name__iexact = forms.MultipleChoiceField(
        label="Abilities (OR)",
        choices=ABILITY_CHOICES,
        required=False
    )

    and_pokemon_moves__name__iexact = forms.MultipleChoiceField(
        label="Moves (AND)",
        choices=MOVE_CHOICES,
        required=False
    )
    or_pokemon_moves__name__iexact = forms.MultipleChoiceField(
        label="Moves (OR)",
        choices=MOVE_CHOICES,
        required=False
    )

    and_pokemon_coverage_moves__type__name__iexact = forms.MultipleChoiceField(
        label="Coverage Move Types (AND)",
        choices=TYPE_CHOICES,
        required=False
    )
    or_pokemon_coverage_moves__type__name__iexact = forms.MultipleChoiceField(
        label="Coverage Move Types (OR)",
        choices=TYPE_CHOICES,
        required=False
    )

    and_pokemon_special_moves__category__iexact = forms.MultipleChoiceField(
        label="Special Move Categories (AND)",
        choices=SpecialMoveCategory.choices,
        required=False
    )
    or_pokemon_special_moves__category__iexact = forms.MultipleChoiceField(
        label="Special Move Categories (OR)",
        choices=SpecialMoveCategory.choices,
        required=False
    )

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__lt___1 = forms.MultipleChoiceField(
        label="Resisted Types (AND)",
        choices=TYPE_CHOICES,
        required=False
    )
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__lt___1 = forms.MultipleChoiceField(
        label="Resisted Types (OR)",
        choices=TYPE_CHOICES,
        required=False
    )

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__gt___1 = forms.MultipleChoiceField(
        label="Weak Types (AND)",
        choices=TYPE_CHOICES,
        required=False
    )
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__gt___1 = forms.MultipleChoiceField(
        label="Weak Types (OR)",
        choices=TYPE_CHOICES,
        required=False
    )

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value___0 = forms.MultipleChoiceField(
        label="Immune Types (AND)",
        choices=TYPE_CHOICES,
        required=False
    )
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value___0 = forms.MultipleChoiceField(
        label="Immune Types (OR)",
        choices=TYPE_CHOICES,
        required=False
    )

class PokemonSimpleSearchForm(forms.Form):
    name__icontains = forms.CharField(label="Name Match", max_length=50, required=False)