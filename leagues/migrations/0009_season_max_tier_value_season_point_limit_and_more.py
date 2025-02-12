# Generated by Django 4.2.16 on 2024-12-27 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0008_alter_league_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='max_tier_value',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='season',
            name='point_limit',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='season',
            name='rules',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='status',
            field=models.CharField(choices=[('PRE_SEASON', 'Pre Season'), ('DRAFT', 'Draft'), ('REGULAR_SEASON', 'Regular Season'), ('PLAYOFFS', 'Playoffs')], default='PRE_SEASON', max_length=15),
        ),
    ]
