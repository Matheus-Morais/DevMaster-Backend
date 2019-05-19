from django.contrib import admin
from .models import Jogador, JogadorItem
from django.contrib.auth.models import User
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

admin.site.register(Jogador)
admin.site.register(JogadorItem)
TokenAdmin.raw_id_fields = ('user',)
