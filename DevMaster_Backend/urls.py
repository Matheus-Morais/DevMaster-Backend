"""DevMaster_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from jogador.api.viewsets import JogadorViewSet, JogadorCreateViewSet, XpeventoViewSet
from jogador.views import JogadorItemViewSet
from missao.api.viewsets import CriarMissaoViewSet, MissaoViewSet
from missao.views import GrupoViewSet
from evento.views import ItemViewSet, EventoViewSet
from desafio.views import DesafioViewSet,DesafioMissaoViewSet

from missao.views import IssueGitlabViewSet

from burndown.views import BurndownViewSet
# , MissaoBurndownViewSet

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'jogador', JogadorViewSet, base_name='jogador')
router.register(r'jogadorxpevento', XpeventoViewSet, base_name='jogadorxpevento')
router.register(r'jogadoritens', JogadorItemViewSet, base_name='jogadoritens')
router.register(r'criarjogador', JogadorCreateViewSet, base_name='jogadorcreate')
router.register(r'criarmissao', CriarMissaoViewSet, base_name='missaocreate')
router.register(r'missao', MissaoViewSet, base_name='missao')
router.register(r'grupo', GrupoViewSet, base_name='grupo')
router.register(r'item', ItemViewSet, base_name='item')
router.register(r'evento', EventoViewSet, base_name='evento')
router.register(r'desafio', DesafioViewSet, base_name='desafio')
router.register(r'missaodesafio', DesafioMissaoViewSet, base_name='missaodesafio')
router.register(r'', IssueGitlabViewSet, base_name='gitlabissue')


router.register(r'burndown', BurndownViewSet, base_name='burndown')

# router.register(r'missaoburndown', MissaoBurndownViewSet, base_name='missaoburndown')
 

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_auth.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
