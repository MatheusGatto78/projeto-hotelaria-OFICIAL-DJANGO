from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Homepage, name='homepage'),
    path('login', views.Login, name='login'),
    path('logout', views.Sair, name='Logout' ),
    path('addquarto', views.addQuarto, name='addquarto'),
    path('addcolaborador', views.add_colaborador, name='addcolaborador'),
    path('quartos', views.quartos, name='quartos'),
    path('reservar/<int:quarto_id>/', views.reservar_quarto, name='reservar_quarto'),
    path('reservar/<int:quarto_id>/', views.reservar_quarto, name='reservar_quarto'),
    path('liberar/<int:quarto_id>/', views.liberar_quarto, name='liberar_quarto'),
    path('quarto/<int:quarto_id>/', views.detalhes_quarto, name='detalhes_quarto'),
    path('editar_quarto/<int:quarto_id>/', views.editar_quarto, name='editar_quarto'),
    path('quarto/excluir/<int:quarto_id>/', views.excluir_quarto, name='excluir_quarto'),
]