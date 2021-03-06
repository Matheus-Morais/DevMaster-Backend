import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions

from desafio.serializers import DesafioSerializer, DesafioMissoesSerializer
from .models import Desafio, DesafioMissoes
from missao.models import Missao

from jogador.models import Jogador, JogadorItem

class DesafioViewSet(GenericViewSet):
    queryset = Desafio.objects.all()
    serializer_class = DesafioSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @action(methods=['POST'], detail=False, url_path='criarDesafio')
    def CriarDesafio(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        if (Jogador.objects.get(user=request.user).tipo == 'J'):
            cadastrado = Desafio.objects.filter(nome=desafio['name'])

            if cadastrado.exists():
                return Response({"error": True, "message": "Esse nome de desafio já está em uso."},status=400)
            else:
                if desafio['is_item']:
                    print(desafio)
                    jogador_item = JogadorItem.objects.get(pk=int(desafio['item_desafiante']))

                    if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                        return Response({"error": True, "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."}, status=400)
                    else:
                        desafiado = Jogador.objects.get(pk=int(desafio['desafiado']))
                        if desafiado.tipo == 'J':
                            jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                            jogador_item.save()

                            newDesafio = Desafio()
                            newDesafio.nome = desafio['name']
                            newDesafio.desafiante = Jogador.objects.get(user=request.user)
                            newDesafio.desafiado = desafiado
                            newDesafio.item_desafiante = jogador_item

                            newDesafio.save()
                            serializer = DesafioSerializer(newDesafio)

                            return Response(serializer.data, status=200)
                        else:
                            return Response({"error": True, "message": "O desafiado não é um jogador."}, status=400)
                else:
                    desafiado = Jogador.objects.get(pk=int(desafio['desafiado']))
                    if desafiado.tipo == 'J':
                        newDesafio = Desafio()
                        newDesafio.nome = desafio['name']
                        newDesafio.desafiante = Jogador.objects.get(user=request.user)
                        newDesafio.desafiado = desafiado

                        newDesafio.save()
                        serializer = DesafioSerializer(newDesafio)

                        return Response(serializer.data, status=200)
                    else:
                        return Response({"error": True, "message": "O desafiado não é um jogador."}, status=400)

        else:
            return Response({"error": True, "message": "Você não tem permissão para Desafiar alguem."},status=400)


    @method_decorator(csrf_exempt)
    @action(methods=['DELETE'], detail=False, url_path='deletarDesafio/(?P<pk>[0-9]+)$')
    def ExcluirDesafio(self, request, pk=None):
        try:
            desafioFinded = Desafio.objects.get(pk=pk)

            if Jogador.objects.get(user=request.user) == desafioFinded.desafiante or Jogador.objects.get(user=request.user) == desafioFinded.desafiado:
                if desafioFinded.status == 'P':
                    desafioFinded.delete()
                    return Response({"message": "Desafio deletado com sucesso."}, status=200)
                else:
                    return Response({"error": True, "message":"O desafio não esta mais em fase de proposta."})
            else:
                return Response({"error": True, "message": "Você não é nem o desafiante, e nem o desafiado, do desafio."}, status=400)
        except Desafio.DoesNotExist:
            return Response({"error": True, "message": "Desafio não existe."}, status=400)


    @method_decorator(csrf_exempt)
    @action(methods=['PUT'], detail=False, url_path='trocarItemDesafio')
    def TrocarItemDesafio(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        if Desafio.objects.get(pk=desafio['id']):
            desafioFinded = Desafio.objects.get(pk=desafio['id'])
            jogadorFinded = Jogador.objects.get(user=request.user)
            if desafioFinded.status == 'P' or desafioFinded.status == 'A':
                if jogadorFinded.tipo == 'J':
                    if jogadorFinded == desafioFinded.desafiado:
                        #quando o jogador vai adicionar o item no desafio pela primeira vez
                        if not desafioFinded.item_desafiado:
                            if desafio['item']:
                                if JogadorItem.objects.get(pk=int(desafio['item'])):
                                    jogador_item = JogadorItem.objects.get(pk=int(desafio['item']))
                                    if jogador_item.jogador == jogadorFinded:
                                        if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                                            return Response({"error": True, "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."}, status=400)
                                        else:
                                            jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                                            jogador_item.save()

                                            desafioFinded.item_desafiado = jogador_item
                                            desafioFinded.status = 'A'
                                            desafioFinded.save()

                                            serializer = DesafioSerializer(desafioFinded)

                                            return Response(serializer.data, status=200)
                                    else:
                                        return Response({"error": True,
                                                        "message": "Esse item não pertence a esse jogador."},
                                                        status=400)
                                else:
                                    return Response({"error": True,
                                                    "message": "Esse item não existe para esse jogador."},
                                                    status=400)
                            else:
                                desafioFinded.item_desafiado = None
                                desafioFinded.status = 'A'
                                desafioFinded.save()

                                serializer = DesafioSerializer(desafioFinded)

                                return Response(serializer.data, status=200)
                        #quando o jogador vai alterar o item do desafio
                        else:
                            if desafio['item']:
                                if JogadorItem.objects.get(pk=int(desafio['item'])):
                                    jogador_item = JogadorItem.objects.get(pk=int(desafio['item']))

                                    if jogador_item.jogador == jogadorFinded:
                                        if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                                            return Response({"error": True,
                                                            "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."},
                                                            status=400)
                                        else:
                                            jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                                            jogador_item.save()

                                            jogador_item_old = JogadorItem.objects.get(pk=desafioFinded.item_desafiado.id)
                                            jogador_item_old.quantidade_bloqueada = jogador_item_old.quantidade_bloqueada - 1
                                            jogador_item_old.save()

                                            desafioFinded.item_desafiado = jogador_item
                                            desafioFinded.status = 'A'
                                            desafioFinded.save()

                                            serializer = DesafioSerializer(desafioFinded)

                                            return Response(serializer.data, status=200)
                                    else:
                                        return Response({"error": True,
                                                        "message": "Esse item não pertence a esse jogador."},
                                                        status=400)
                                else:
                                    return Response({"error": True,
                                                    "message": "Esse item não existe para esse jogador."},
                                                    status=400)
                            else:
                                desafioFinded.item_desafiado = None
                                desafioFinded.status = 'A'
                                desafioFinded.save()

                                serializer = DesafioSerializer(desafioFinded)

                                return Response(serializer.data, status=200)
                    elif jogadorFinded == desafioFinded.desafiante:
                        # quando o jogador vai adicionar o item no desafio pela primeira vez
                        if not desafioFinded.item_desafiante:
                            if desafio['item']:
                                if JogadorItem.objects.get(pk=int(desafio['item'])):
                                    jogador_item = JogadorItem.objects.get(pk=int(desafio['item']))
                                    if jogador_item.jogador == jogadorFinded:
                                        if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                                            return Response({"error": True,
                                                            "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."},
                                                            status=400)
                                        else:
                                            jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                                            jogador_item.save()

                                            desafioFinded.item_desafiante = jogador_item
                                            desafioFinded.save()

                                            serializer = DesafioSerializer(desafioFinded)

                                            return Response(serializer.data, status=200)
                                    else:
                                        return Response({"error": True,
                                                        "message": "Esse item não pertence a esse jogador."},
                                                        status=400)
                                else:
                                    return Response({"error": True,
                                                    "message": "Esse item não existe para esse jogador."},
                                                    status=400)
                            else:
                                desafioFinded.item_desafiante = None
                                desafioFinded.save()
                                serializer = DesafioSerializer(desafioFinded)

                                return Response(serializer.data, status=200)
                        # quando o jogador vai alterar o item do desafio
                        else:
                            if desafio['item']:
                                if JogadorItem.objects.get(pk=int(desafio['item'])):
                                    jogador_item = JogadorItem.objects.get(pk=int(desafio['item']))

                                    if jogador_item.jogador == jogadorFinded:
                                        if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                                            return Response({"error": True,
                                                            "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."},
                                                            status=400)
                                        else:
                                            jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                                            jogador_item.save()

                                            jogador_item_old = JogadorItem.objects.get(pk=desafioFinded.item_desafiante.id)
                                            jogador_item_old.quantidade_bloqueada = jogador_item_old.quantidade_bloqueada - 1
                                            jogador_item_old.save()

                                            desafioFinded.item_desafiante = jogador_item
                                            desafioFinded.save()

                                            serializer = DesafioSerializer(desafioFinded)

                                            return Response(serializer.data, status=200)
                                    else:
                                        return Response({"error": True,
                                                        "message": "Esse item não pertence a esse jogador."},
                                                        status=400)
                                else:
                                    return Response({"error": True,
                                                    "message": "Esse item não existe para esse jogador."},
                                                    status=400)
                            else:
                                desafioFinded.item_desafiante = None
                                desafioFinded.save()
                                serializer = DesafioSerializer(desafioFinded)

                                return Response(serializer.data, status=200)
                    else:
                        return Response({"error": True,
                                         "message": "Você não é nem o desafiante e nem o desafiado."},
                                        status=400)
                else:
                    return Response({"error": True, "message": "Você não é um jogador."}, status=400)
            else:
                return Response({"error": True, "message": "O desafio não esta nesse estagio."}, status=400)
        else:
            return Response({"error": True, "message": "Desafio não existe."}, status=400)


    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='listarDesafios')
    def ListarDesafios(self, request):
        jogadorFinded = Jogador.objects.get(user=request.user)
        desafios = Desafio.objects.filter(desafiante=jogadorFinded) | Desafio.objects.filter(desafiado=jogadorFinded)

        serializer = DesafioSerializer(desafios, many=True)

        return Response({'List': serializer.data})


    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='consultarDesafios')
    def ConsultarDesafios(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        jogadorFinded = Jogador.objects.get(user=request.user)
        desafioFinded = Desafio.objects.get(pk=desafio['id'])

        if jogadorFinded == desafioFinded.desafiante or jogadorFinded == desafioFinded.desafiado:

            serializer = DesafioSerializer(desafioFinded)
            return Response({'Desafio': serializer.data})
        else:
            return Response({"error": True,
                             "message": "Esse desafio não pertence a você."},
                            status=400)

    @method_decorator(csrf_exempt)
    @action(methods=['PUT'], detail=False, url_path='mudarStatus')
    def MudarStatus(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        if Desafio.objects.get(pk=desafio['id']):
            desafioFinded = Desafio.objects.get(pk=desafio['id'])
            if desafio['status'] == 'E':
                if desafioFinded.status == 'A':
                    desafioFinded.status = 'E'
                    desafioFinded.save()

                    serializer = DesafioSerializer(desafioFinded)
                    return Response({'Desafio': serializer.data}, status=200)
                else:
                    return Response({"error": True, "message": "Desafio não esta em fase de aposta."}, status=400)

            elif desafio['status'] == 'C':
                if desafioFinded.status == 'E':
                    missoesdesafioFinded = DesafioMissoes.objects.filter(desafio=desafioFinded)

                    aux_desafiante = 0
                    aux_desafiado = 0

                    for mFinded in missoesdesafioFinded:
                        if mFinded.desafio.desafiante == mFinded.missao.jogador:
                            aux_desafiante = aux_desafiante + mFinded.xp_ganha

                        if mFinded.desafio.desafiado == mFinded.missao.jogador:
                            aux_desafiado = aux_desafiado + mFinded.xp_ganha

                    if aux_desafiante > aux_desafiado:
                        desafioFinded.vencedor = 'DE'

                        jogadorVencedor = Jogador.objects.get(pk=desafioFinded.desafiante.id)
                        jogadorVencedor.desafios_v = jogadorVencedor.desafios_v + 1
                        jogadorVencedor.save()

                        if desafioFinded.item_desafiado:
                            if JogadorItem.objects.filter(jogador=desafioFinded.desafiante,item=desafioFinded.item_desafiado.item):
                                jogadorItem_Desafiante = JogadorItem.objects.get(jogador=desafioFinded.desafiante,item=desafioFinded.item_desafiado.item)
                                jogadorItem_Desafiante.quantidade = jogadorItem_Desafiante.quantidade + 1
                                if jogadorItem_Desafiante == desafioFinded.item_desafiado:
                                    jogadorItem_Desafiante.quantidade_bloqueada = jogadorItem_Desafiante.quantidade_bloqueada - 1

                                jogadorItem_Desafiante.save()

                            else:
                                newJogadorItem_desafiante = JogadorItem()
                                newJogadorItem_desafiante.item = desafioFinded.item_desafiado.item
                                newJogadorItem_desafiante.jogador = desafioFinded.desafiante
                                newJogadorItem_desafiante.quantidade = 1
                                newJogadorItem_desafiante.quantidade_bloqueada = 0
                                newJogadorItem_desafiante.save()

                        if desafioFinded.item_desafiante:
                            jogadorItem_Desafiante_2 = JogadorItem.objects.get(jogador=desafioFinded.desafiante,item=desafioFinded.item_desafiante.item)
                            jogadorItem_Desafiante_2.quantidade_bloqueada = jogadorItem_Desafiante_2.quantidade_bloqueada - 1
                            jogadorItem_Desafiante_2.save()

                        if desafioFinded.item_desafiado:
                            jogadorItem_Desafiado = JogadorItem.objects.get(jogador=desafioFinded.desafiado,item=desafioFinded.item_desafiado.item)
                            jogadorItem_Desafiado.quantidade = jogadorItem_Desafiado.quantidade - 1
                            jogadorItem_Desafiado.quantidade_bloqueada = jogadorItem_Desafiado.quantidade_bloqueada - 1
                            jogadorItem_Desafiado.save()

                    elif aux_desafiante < aux_desafiado:
                        desafioFinded.vencedor = 'DO'

                        jogadorVencedor = Jogador.objects.get(pk=desafioFinded.desafiado.id)
                        jogadorVencedor.desafios_v = jogadorVencedor.desafios_v + 1
                        jogadorVencedor.save()

                        if desafioFinded.item_desafiante:
                            if JogadorItem.objects.filter(jogador=desafioFinded.desafiado,item=desafioFinded.item_desafiante.item):
                                jogadorItem_Desafiado = JogadorItem.objects.get(jogador=desafioFinded.desafiado,item=desafioFinded.item_desafiante.item)
                                jogadorItem_Desafiado.quantidade = jogadorItem_Desafiado.quantidade + 1

                                if jogadorItem_Desafiado == desafioFinded.item_desafiante:
                                    jogadorItem_Desafiado.quantidade_bloqueada = jogadorItem_Desafiado.quantidade_bloqueada - 1

                                jogadorItem_Desafiado.save()

                            else:
                                newJogadorItem_desafiado = JogadorItem()
                                newJogadorItem_desafiado.item = desafioFinded.item_desafiante.item
                                newJogadorItem_desafiado.jogador = desafioFinded.desafiado
                                newJogadorItem_desafiado.quantidade = 1
                                newJogadorItem_desafiado.quantidade_bloqueada = 0
                                newJogadorItem_desafiado.save()

                            if desafioFinded.item_desafiado:
                                jogadorItem_Desafiado_2 = JogadorItem.objects.get(jogador=desafioFinded.desafiado,item=desafioFinded.item_desafiado.item)
                                jogadorItem_Desafiado_2.quantidade_bloqueada = jogadorItem_Desafiado_2.quantidade_bloqueada - 1
                                jogadorItem_Desafiado_2.save()

                            if desafioFinded.item_desafiante:
                                jogadorItem_Desafiante = JogadorItem.objects.get(jogador=desafioFinded.desafiante,item=desafioFinded.item_desafiante.item)
                                jogadorItem_Desafiante.quantidade = jogadorItem_Desafiante.quantidade - 1
                                jogadorItem_Desafiante.quantidade_bloqueada = jogadorItem_Desafiante.quantidade_bloqueada - 1
                                jogadorItem_Desafiante.save()

                    else:
                        desafioFinded.vencedor = 'EM'
                        if desafioFinded.item_desafiado:
                            jogadorItem_Desafiado = JogadorItem.objects.get(jogador=desafioFinded.desafiado,item=desafioFinded.item_desafiado.item)
                            jogadorItem_Desafiado.quantidade_bloqueada = jogadorItem_Desafiado.quantidade_bloqueada - 1
                            jogadorItem_Desafiado.save()

                        if desafioFinded.item_desafiante:
                            jogadorItem_Desafiante = JogadorItem.objects.get(jogador=desafioFinded.desafiante,item=desafioFinded.item_desafiante.item)
                            jogadorItem_Desafiante.quantidade_bloqueada = jogadorItem_Desafiante.quantidade_bloqueada - 1
                            jogadorItem_Desafiante.save()

                    desafioFinded.status = 'C'
                    desafioFinded.save()

                    serializer = DesafioSerializer(desafioFinded)
                    return Response({'Desafio': serializer.data}, status=200)
                else:
                    return Response({"error": True, "message": "Desafio não esta em fase de andamento."}, status=400)
        else:
            return Response({"error": True, "message": "Desafio não existe."}, status=400)


class DesafioMissaoViewSet(GenericViewSet):
    queryset = DesafioMissoes.objects.all()
    serializer_class = DesafioMissoesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @action(methods=['POST'], detail=False, url_path='addMissoesDesafio')
    def AddMissoesDesafio(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        if Desafio.objects.get(pk=desafio['id_desafio']):
            desafioFinded = Desafio.objects.get(pk=desafio['id_desafio'])
            jogadorFinded = Jogador.objects.get(user=request.user)
            missaoFinded = Missao.objects.get(pk=desafio['id_missao'])
            if not missaoFinded.status:
                if desafioFinded.status == 'A':
                    if jogadorFinded.tipo == 'J':
                        if len(DesafioMissoes.objects.filter(desafio=desafioFinded,missao=missaoFinded)) == 0:
                            if jogadorFinded == desafioFinded.desafiado or jogadorFinded == desafioFinded.desafiante:
                                if jogadorFinded == missaoFinded.jogador:
                                    newDesafioMissao = DesafioMissoes()
                                    newDesafioMissao.desafio = desafioFinded
                                    newDesafioMissao.missao = missaoFinded

                                    newDesafioMissao.save()
                                    serializer = DesafioMissoesSerializer(newDesafioMissao)

                                    return Response(serializer.data, status=200)
                                else:
                                    return Response({"error": True, "message": "Você não é o dono dessa missão."},
                                                    status=400)
                            else:
                                return Response({"error": True,
                                                 "message": "Você não é nem o desafiante e nem o desafiado."},
                                                status=400)
                        else:
                            return Response({"error": True, "message": "Esse desafio ja tem essa missão."}, status=400)
                    else:
                        return Response({"error": True, "message": "Você não é um jogador."}, status=400)
                else:
                    return Response({"error": True, "message": "O desafio não esta nesse estagio."}, status=400)
            else:
                return Response({"error": True, "message": "Essa missão já foi finalizada."}, status=400)
        else:
            return Response({"error": True, "message": "Desafio não existe."}, status=400)


    @method_decorator(csrf_exempt)
    @action(methods=['DELETE'], detail=False, url_path='deleteMissoesDesafio/(?P<pk>[0-9]+)$')
    def DeleteMissoesDesafio(self, request, pk=None):
        try:
            desafioMissaoFinded = DesafioMissoes.objects.get(pk=pk)

            if Jogador.objects.get(user=request.user) == desafioMissaoFinded.missao.jogador:
                desafioMissaoFinded.delete()

                return Response({"message": "Desafio deletado com sucesso."}, status=200)
            else:
                return Response({"error": True, "message": "Você não é o desafiante do desafio."}, status=400)
        except Desafio.DoesNotExist:
            return Response({"error": True, "message": "Desafio não existe."}, status=400)


    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='consultarMissoesDesafio/(?P<pk>[0-9]+)$')
    def ConsultarMissoesDesafio(self, request, pk=None):
        try:
            desafioFinded = Desafio.objects.get(pk=pk)
            missoesDesafioFinded = DesafioMissoes.objects.filter(desafio=desafioFinded)

            serializer = DesafioMissoesSerializer(missoesDesafioFinded, many=True)

            return Response({'List': serializer.data})

        except Desafio.DoesNotExist:
            return Response({"error": True, "message": "Desafio não existe."}, status=400)