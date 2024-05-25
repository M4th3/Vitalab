from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TiposExames, SolicitacaoExame, PedidosExames, AcessoMedico
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
import datetime


#admin usuario: matheus
#admin senha  : pires
#usuario usuario: guimê
#usuario senha  : 12345678

@login_required(login_url='/usuarios/login')
def solicitar_exame(request):

    if request.method == "GET":
        tipos_exames = TiposExames.objects.all()
        return render(request, 'html/solicitar_exames.html', {'tipos_exames':tipos_exames})
    
    else:
        tipos_exames = TiposExames.objects.all()
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        data = datetime.datetime.now()
        preco_total = 0
        for i in solicitacao_exames:
            if i.disponivel:
                preco_total += i.preco
        
        return render(request, 'html/solicitar_exames.html', {'tipos_exames':tipos_exames,
                                                              'solicitacao_exames':solicitacao_exames,
                                                              'preco_total':preco_total, 'data': data}
                                                              )
    
def logout_conta(request):
    logout(request)
    return redirect('/usuarios/login')

@login_required(login_url='/usuarios/login')    
def fechar_pedido(request):
    id_exames = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=id_exames)
    print('###############Parou aqui1###############')
    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.datetime.now()
    )
    print('###############Parou aqui2###############')
    pedido_exame.save()

    for exame in solicitacao_exames:

        solicitacao_exames_temp = SolicitacaoExame(
            usuario = request.user,
            exame = exame,
            status = "E"
        )

        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)

    pedido_exame.save()

    messages.add_message(request, messages.constants.SUCCESS, 'Pedido de exame concluído com sucesso !!!')
    return redirect('/exames/gerenciar_pedidos')

@login_required(login_url='/usuarios/login')        
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'html/gerenciar_pedidos.html', {'pedidos_exames':pedidos_exames})    

@login_required(login_url='/usuarios/login')
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)
    if not pedido.usuario == request.user:
        messages.add_message(request, messages.constants.ERROR, 'Esse pedido não é seu!!!')
        return redirect('/exames/gerenciar_pedidos')
    pedido.agendado = False
    pedido.save()
    messages.add_message(request, messages.constants.SUCCESS, 'Seu pedido foi cancelado !!!')
    return redirect('/exames/gerenciar_pedidos')

@login_required(login_url='/usuarios/login')            
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)
    
    
    return render(request, 'html/gerenciar_exames.html', {'exames': exames})

@login_required(login_url='/usuarios/login')
def permitir_abrir_exame(request, exame_id):
    exame =SolicitacaoExame.objects.get(id=exame_id)

    if exame.usuario != request.user:
        return redirect('/exames/gerenciar_exames')
    
    if not exame.requer_senha:
        print(f'#############url do exame: {exame.resultado.url}############')
        return redirect(exame.resultado.url)
       
    else:
        return redirect(f'/exames/solicitar_senha_exame/{exame_id}')

@login_required(login_url='/usuarios/login')    
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if request.method == 'GET':
        print(f'####################{exame.resultado.url}###################')
        return render(request, 'html/solicitar_senha_exame.html', {'exame': exame})    
    elif request.method == 'POST':
        if exame.usuario == request.user:
            senha = request.POST.get('senha')
            if exame.senha == senha:
                return redirect(exame.resultado.url)
            else:
                messages.add_message(request, messages.constants.ERROR, 'A senha está errada!!!')
                return redirect(f'/exames/solicitar_senha_exame/{exame.id}')
        else:
            messages.add_message(request, messages.constants.ERROR, 'Você não tem permissão para acessar essa página!!!')
            return redirect('/exames/gerenciar_exames')

@login_required(login_url='/usuarios/login')
def gerar_acesso_medico(request):
    if request.method == 'GET':
        acessos = AcessoMedico.objects.filter(usuario=request.user)
        return render(request, 'html/gerar_acesso_medico.html', {'acessos': acessos})
    elif request.method == 'POST':
        print('------------------------- REQUEST POST -----------------------------------')
        print(request.POST)
        print('--------------------------------------------------------------------------')
        identificacao = request.POST.get('identificacao')
        tempo_de_acesso = request.POST.get('tempo_de_acesso')
        data_exame_inicial = request.POST.get('data_exame_inicial')
        data_exame_final = request.POST.get('data_exame_final')

        acesso_medico = AcessoMedico(
            usuario=request.user, 
            identificacao=identificacao, 
            tempo_de_acesso=tempo_de_acesso, 
            data_exames_iniciais=data_exame_inicial, 
            date_exames_finais=data_exame_final, 
            criado_em=datetime.datetime.now()
        )

        acesso_medico.save()

        messages.add_message(request, messages.constants.SUCCESS, "Acesso criado com sucesso!!!")
        return redirect('/exames/gerar_acesso_medico')
    
    
    
