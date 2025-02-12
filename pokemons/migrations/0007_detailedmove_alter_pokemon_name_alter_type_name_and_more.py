# Generated by Django 4.2.16 on 2025-01-12 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0006_pokemontypeeffective_delete_pokemontypeweakness'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailedMove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('base_power', models.IntegerField()),
                ('accuracy', models.IntegerField()),
                ('pp', models.IntegerField()),
                ('priority', models.IntegerField()),
                ('category', models.CharField(choices=[('physical', 'Physical'), ('special', 'Special'), ('status', 'Status')], max_length=8)),
                ('special_category', models.CharField(blank=True, choices=[('momentum', 'Momentum'), ('recovery', 'Recovery'), ('cleric', 'Cleric'), ('hazard', 'Hazard'), ('hazard removal', 'Hazard Removal'), ('disruption', 'Disruption'), ('damage reduction', 'Damage Reduction'), ('set up', 'Set Up'), ('priority', 'Priority'), ('item removal', 'Item Removal'), ('status', 'Status')], max_length=16, null=True)),
                ('viable', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.CreateModel(
            name='PokemonDetailedMove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('detailed_move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_detailed_moves', to='pokemons.detailedmove')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_detailed_moves', to='pokemons.pokemon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='detailedmove',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detailed_moves', to='pokemons.type'),
        ),
    ]
