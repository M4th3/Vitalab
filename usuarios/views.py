from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login



# Create your views here.

def cadastro(request):

    if request.method == 'GET':
        return render(request, 'html/cadastro.html')
    
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem!!!')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha precisa de no mínimo 6 caracteres!!!')
            return redirect('/usuarios/cadastro')
        
        try:
            user = User.objects.create_user(first_name=primeiro_nome, last_name=ultimo_nome, username=username, email=email, password=senha,)
            print('------------------------Try executado--------------------------------------- ')
        except: 
            print('----------------------try falhou-----------------------')
            return redirect('/usuarios/cadastro')

        return redirect('/usuarios/login')     
    
def logar(request):
    if request.method == 'GET':
        return render(request, 'html/login.html')
    
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user:
            login(request, user)
            return redirect("/exames/solicitar_exames")

        else:
            messages.add_message(request, constants.ERROR, "Falha na autenticação, algum dado inserido está incorreto, ou o usuário não a existe!!!")                
            return redirect('/usuarios/login')




        
        

    
