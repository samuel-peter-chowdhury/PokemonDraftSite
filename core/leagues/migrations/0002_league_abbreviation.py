# Generated by Django 4.2.16 on 2024-12-01 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='abbreviation',
            field=models.CharField(default='NL', max_length=4),
            preserve_default=False,
        ),
    ]
