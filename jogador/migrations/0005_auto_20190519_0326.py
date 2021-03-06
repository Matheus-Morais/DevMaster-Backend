# Generated by Django 2.2.1 on 2019-05-19 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0002_auto_20190519_0326'),
        ('jogador', '0004_jogador_desafios_v'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogador',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='XpEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xp_evento', models.FloatField(blank=True, default=0)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Evento', to='evento.Evento')),
                ('jogador', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='JogadorEventoXP', to='jogador.Jogador')),
            ],
        ),
    ]
