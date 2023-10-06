from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'as senhas não são iguais')
            return redirect ('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'sua senha deve ter 6 ou mais digitos')
            return redirect ('/usuarios/cadastro')
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, 'Este nome de usuário já está em uso.')
            return redirect('/usuarios/cadastro')

        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username = username,
                email = email,
                password = senha,
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário salvo com sucesso!')
            return redirect('/usuarios/login')
        except:
            messages.add_message(request, constants.ERROR, 'erro interno do sistema, contate um administrador')
            return redirect ('/usuarios/cadastro')
    
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
            return redirect('/') #provisorio
        else:
           messages.add_message(request, constants.ERROR, 'Usuário ou senha incorreto')
           return redirect('usuarios/login')