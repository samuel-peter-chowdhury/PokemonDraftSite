# Generated by Django 4.2.16 on 2024-12-01 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leagues', '0003_alter_league_logo_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, default='default_team_logo.png', upload_to='')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='leagues.season')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
