# Generated by Django 2.2.1 on 2019-05-26 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missao', '0006_auto_20190526_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missao',
            name='id_milestone',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
