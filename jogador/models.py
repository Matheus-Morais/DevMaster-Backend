from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from evento.models import Item, Evento

class Jogador(models.Model):
    """Essa classe se destina para o cadastro de Jogador"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='User', blank = True)
    tipo = models.CharField(verbose_name='Tipo', max_length=1, default='J', blank=True)
    xp_total = models.FloatField(default=0, blank=True)
    desafios_v = models.IntegerField(default=0, blank=True)
    eventos_v = models.IntegerField(default=0, blank=True)
    m_realizadas = models.IntegerField(default=0, blank=True)
    m_adquiridas = models.IntegerField(default=0, blank=True)
    mr_nadata = models.IntegerField(default=0, blank=True)
    private_token = models.CharField(blank=False, max_length=100)
    url_imagem = models.CharField(blank=False, max_length=300, default='')

    def __str__(self):
        return 'Jogador: %s' % (self.user.get_full_name())

class JogadorItem(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='JogadorItem')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemJogador')
    quantidade = models.IntegerField(default=0)
    quantidade_bloqueada = models.IntegerField(default=0)

    def __str__(self):
        return 'Jogador: ' + self.jogador.user.get_full_name() + ' - Item: ' + self.item.name

class XpEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT, related_name='Evento')
    jogador = models.ForeignKey(Jogador, blank=True, on_delete=models.CASCADE, related_name='JogadorEventoXP')
    xp_evento = models.FloatField(default=0, blank=True)

    def __str__(self):
        return 'Evento: ' + self.evento.name + ' - Jogador: ' + self.jogador.user.get_full_name()
