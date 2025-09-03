from django.urls import include, path 
from contas import views

urlpatterns = [
    path('timeout/',  views.timeout_view, name='timeout'), 
    path('login/',  views.login_view, name='login'), 
    path('criar-conta/',  views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'),
    path('atualizar-usuario/', views.atualizar_meu_usuario, name='atualizar_meu_usuario'),
    path('atualizar-usuario/<int:user_id>/', views.atualizar_usuario, name='atualizar_usuario'),
    path('lista-usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('', include("django.contrib.auth.urls")), #Django Auth
]