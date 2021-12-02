from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
# Create your views here.


#def index(request):
#    return redirect('/agenda')

def login_user(request):
    return render(request, 'login.html')

def logout_user(resquest):
    logout(resquest)
    return redirect('/') # redireciona para o indice

def submit_login(request):
    if request.POST:# se a requisição for um POST
        username = request.POST.get('username') #pega dados da requisição
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido")
    return redirect('/')



#decorador, roda o código só se tiver um user logado, se não tiver
# redireciona para login/
@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user

    #evento = Evento.objects.get(id=1)
    #response = {'evento': evento}
    data_atual = datetime.now() - timedelta(hours=1)
    eventos = Evento.objects.filter(usuario=usuario)

 #                                   data_evento__gt=data_atual) #gt pega datas futuras, lt datas antigas

    dados = {'eventos': eventos}

    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario: #se o evento for do usuário logado
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.local = local
                evento.save()

#            Evento.objects.filter(id=id_evento).update(
#                titulo=titulo,
#                data_evento=data_evento,
#               descricao=descricao,
#                local=local,
#            )

        else:
            Evento.objects.create(
                titulo=titulo,
                data_evento=data_evento,
                descricao=descricao,
                local=local,
                usuario=usuario
            )

    return redirect('/') #/agenda

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404
    if usuario == evento.usuario: #identifica se o evento é mesmo do usuário
        evento.delete()
    else:
        raise Http404
    return redirect('/')#/agenda


@login_required(login_url='/login/')
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')

    return JsonResponse(list(evento), safe=False)