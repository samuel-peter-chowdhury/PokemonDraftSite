# Generated by Django 4.2.16 on 2024-12-01 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0002_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonTypeWeakness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.FloatField()),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_type_weaknesses', to='pokemons.pokemon')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_type_weaknesses', to='pokemons.type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PokemonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_types', to='pokemons.pokemon')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_types', to='pokemons.type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PokemonSpecialMove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(choices=[('momentum', 'Momentum'), ('recovery', 'Recovery'), ('cleric', 'Cleric'), ('hazard', 'Hazard'), ('hazard removal', 'Hazard Removal'), ('disruption', 'Disruption'), ('damage reduction', 'Damage Reduction'), ('set up', 'Set Up'), ('priority', 'Priority'), ('item removal', 'Item Removal'), ('status', 'Status')], max_length=16)),
                ('name', models.CharField(max_length=50)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_special_moves', to='pokemons.pokemon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PokemonMove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_moves', to='pokemons.pokemon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PokemonCoverageMove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_coverage_moves', to='pokemons.pokemon')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_coverage_moves', to='pokemons.type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PokemonAbility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_abilities', to='pokemons.pokemon')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
