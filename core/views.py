from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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

    eventos = Evento.objects.filter(usuario=usuario)

    dados ={'eventos': eventos}

    return render(request, 'agenda.html', dados)
