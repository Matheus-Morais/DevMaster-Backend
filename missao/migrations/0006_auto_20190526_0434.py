# Generated by Django 2.2.1 on 2019-05-26 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missao', '0005_missao_id_milestone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missao',
            name='id_milestone',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
