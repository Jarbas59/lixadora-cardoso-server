from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from contas.models import MyUser
from contas.permissions import grupo_colaborador_required
from django.core.mail import send_mail

from apps.contas.forms import CustomUserCreationForm
from apps.contas.forms import UserChangeForm

def timeout_view(request):
    return render(request, 'timeout.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

# Registrar um usuário:
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.is_active = False
            usuario.save()
            
            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            
            send_mail( # Envia email para usuario
                'Cadastro Plataforma',
                f'Olá, {usuario.first_name}, em breve você receberá um e-mail de aprovação para usar a plataforma.',
                'workingnicolasp@gmail.com',
                [usuario.email],
                fail_silently=False,
            )
            
            send_mail( # Envia email para admin
                'Novo Cadastro Plataforma',
                f'Olá, Administrador! Há um novo usuário no sistema, Nome: {usuario.first_name}, E-mail: {[usuario.email]}, dê as boas vindas e aceite-o.',
                'workingnicolasp@gmail.com',
                ['workingnicolasp@gmail.com'],
                fail_silently=False,
            )
    
            messages.success(request, 'Registrado. Um e-mail foi enviado para o administrador aprovar. Aguarde contato')
            return redirect('login')
        else:
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
                1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm()
    return render(request, "register.html",{"form": form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required()
def atualizar_meu_usuario(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user, user=request.user)
    return render(request, 'user_update.html', {'form': form})

# Atualizar usuário passa um parametro ID de qualquer usuario
@login_required()
@grupo_colaborador_required(['Administrador','Colaborador'])
def atualizar_usuario(request, user_id):
    user = get_object_or_404(MyUser, pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=user, user=request.user)
    return render(request, 'user_update.html', {'form': form})

@login_required
@grupo_colaborador_required(['Administrador','Colaborador'])
def lista_usuarios(request): # Lista Cliente 
	lista_usuarios = MyUser.objects.filter(is_superuser=False) 
	return render(request, 'lista-usuarios.html', {'lista_usuarios': lista_usuarios})