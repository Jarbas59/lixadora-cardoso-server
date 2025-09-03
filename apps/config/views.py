from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from contas.permissions import grupo_colaborador_required

@login_required
@grupo_colaborador_required(['Administrador','Colaborador'])
def painel_view(request):
    return render(request, 'painel.html')

@login_required
@grupo_colaborador_required(['Administrador','Colaborador'])
def configuracao_view(request):
    return render(request, 'configuracao.html')