# Generated by Django 2.2.1 on 2019-05-26 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missao', '0004_auto_20190526_0359'),
    ]

    operations = [
        migrations.AddField(
            model_name='missao',
            name='id_milestone',
            field=models.IntegerField(default=0),
        ),
    ]
