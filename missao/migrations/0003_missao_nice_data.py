# Generated by Django 2.2.1 on 2019-05-26 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missao', '0002_missao_xp_ganha'),
    ]

    operations = [
        migrations.AddField(
            model_name='missao',
            name='nice_data',
            field=models.BooleanField(default=False),
        ),
    ]
