from django import forms

from .models import Team
from pokemons.models import SpecialMoveCategory, Type, PokemonAbility, PokemonMove, DetailedMove

TYPE_CHOICES = [(t.name.capitalize(), t.name.capitalize()) for t in Type.objects.all().order_by('name')]
ABILITY_CHOICES = [(x['name'].capitalize(), x['name'].capitalize()) for x in PokemonAbility.objects.values('name').distinct().order_by('name')]
MOVE_CHOICES = [(x['name'].capitalize(), x['name'].capitalize()) for x in PokemonMove.objects.values('name').distinct().order_by('name')]
DETAILED_MOVE_CHOICES = [(x['name'].capitalize(), x['name'].capitalize()) for x in DetailedMove.objects.values('name').distinct().order_by('name')]

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
    base_name__icontains = forms.CharField(label="Name Match", max_length=50, required=False, widget=forms.TextInput(attrs={'style': 'width: 10rem'}))

    base_hp__gte = forms.IntegerField(label="Min HP", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_hp__lte = forms.IntegerField(label="Max HP", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_attack__gte = forms.IntegerField(label="Min Atk", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_attack__lte = forms.IntegerField(label="Max Atk", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_defense__gte = forms.IntegerField(label="Min Def", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_defense__lte = forms.IntegerField(label="Max Def", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_special_attack__gte = forms.IntegerField(label="Min SpA", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_special_attack__lte = forms.IntegerField(label="Max SpA", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_special_defense__gte = forms.IntegerField(label="Min SpD", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_special_defense__lte = forms.IntegerField(label="Max SpD", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_speed__gte = forms.IntegerField(label="Min Spd", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_speed__lte = forms.IntegerField(label="Max Spd", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_base_stat_total__gte = forms.IntegerField(label="Min BST", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_base_stat_total__lte = forms.IntegerField(label="Max BST", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_point_value__gte = forms.IntegerField(label="Min Pts", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))
    base_point_value__lte = forms.IntegerField(label="Max Pts", required=False, widget=forms.NumberInput(attrs={'style': 'width: 5rem'}))

    and_pokemon_types__type__name__iexact = forms.MultipleChoiceField(
        label="Types (&)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    or_pokemon_types__type__name__iexact = forms.MultipleChoiceField(
        label="Types (|)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )

    and_pokemon_abilities__name__iexact = forms.MultipleChoiceField(
        label="Abilities (&)",
        choices=ABILITY_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    or_pokemon_abilities__name__iexact = forms.MultipleChoiceField(
        label="Abilities (|)",
        choices=ABILITY_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )

    and_pokemon_detailed_moves__detailed_move__name__iexact = forms.MultipleChoiceField(
        label="Moves (&)",
        choices=DETAILED_MOVE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    or_pokemon_detailed_moves__detailed_move__name__iexact = forms.MultipleChoiceField(
        label="Moves (|)",
        choices=DETAILED_MOVE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )

    and_pokemon_detailed_moves__detailed_move__type__name__iexact = forms.MultipleChoiceField(
        label="Type Moves (&)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    or_pokemon_detailed_moves__detailed_move__type__name__iexact = forms.MultipleChoiceField(
        label="Type Moves (|)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )

    and_pokemon_detailed_moves__detailed_move__special_category__iexact = forms.MultipleChoiceField(
        label="Special Moves (&)",
        choices=SpecialMoveCategory.choices,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    or_pokemon_detailed_moves__detailed_move__special_category__iexact = forms.MultipleChoiceField(
        label="Special Moves (|)",
        choices=SpecialMoveCategory.choices,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__lt___1 = forms.MultipleChoiceField(
        label="Resisted Types (&)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__lt___1 = forms.MultipleChoiceField(
        label="Resisted Types (|)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__gt___1 = forms.MultipleChoiceField(
        label="Weak Types (&)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value__gt___1 = forms.MultipleChoiceField(
        label="Weak Types (|)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )

    and_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value___0 = forms.MultipleChoiceField(
        label="Immune Types (&)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    or_pokemon_type_effectives__type__name__iexact___pokemon_type_effectives__value___0 = forms.MultipleChoiceField(
        label="Immune Types (|)",
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 10rem'})
    )
    exclude_drafted_pokemon = forms.BooleanField(
        label="Exclude Drafted Pokemon",
        required=False,
        initial=True
    )

class PokemonSimpleSearchForm(forms.Form):
    name__icontains = forms.CharField(label="Name Match", max_length=50, required=False)