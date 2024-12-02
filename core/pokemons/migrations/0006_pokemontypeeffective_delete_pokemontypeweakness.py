# Generated by Django 4.2.16 on 2024-12-02 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0005_alter_pokemon_condition_alter_pokemon_dex_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonTypeEffective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.FloatField()),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_type_effectives', to='pokemons.pokemon')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_type_effectives', to='pokemons.type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='PokemonTypeWeakness',
        ),
    ]
