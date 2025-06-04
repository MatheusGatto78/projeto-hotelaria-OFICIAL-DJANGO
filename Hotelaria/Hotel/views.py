from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden

# PÁGINA INICIAL
def Homepage(request):
    dados_home = homepage.objects.all()
    return render(request, 'homepage.html', {'dados_home': dados_home})

# LOGIN
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage') 
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos.'})
    return render(request, 'login.html')


def Sair(request):
    logout(request)
    return redirect('homepage')


def is_gerente(user):
    return user.is_authenticated and user.groups.filter(name='Gerente').exists()


def is_colaborador(user):
    return user.is_authenticated and user.groups.filter(name='Colaborador').exists()


@user_passes_test(is_gerente, login_url='/')
def addQuarto(request):
    if request.method == "POST":
        cadastro = quartoForms(request.POST, request.FILES)
        if cadastro.is_valid():
            cadastro.save()
            return redirect('addquarto')
    else:
        cadastro = quartoForms()
    return render(request, 'add_quartos.html', {'form': cadastro})


@login_required(login_url='/')
def add_colaborador(request):
    if not is_gerente(request.user):
        return HttpResponseForbidden("Apenas gerentes podem adicionar colaboradores.")
    
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            grupo, created = Group.objects.get_or_create(name='Colaborador')
            user.groups.add(grupo)

            return redirect('homepage')
    else:
        form = ColaboradorForm()
    
    return render(request, 'add_colaborador.html', {'form': form})


@login_required(login_url='/')
def quartos(request):
    quartos = quarto.objects.all()
    return render(request, 'quartos.html', {'quartos': quartos})

@login_required(login_url='/')
def detalhes_quarto(request, quarto_id):
    q = get_object_or_404(quarto, id=quarto_id)
    try:
        reserva = Reserva.objects.get(quarto=q)
    except Reserva.DoesNotExist:
        reserva = None
    return render(request, 'detalhes_quarto.html', {'quarto': q, 'reserva': reserva})



@login_required(login_url='/')
def reservar_quarto(request, quarto_id):
    user = request.user
    q = get_object_or_404(quarto, id=quarto_id)

    if not user.groups.filter(name__in=['Gerente', 'Colaborador']).exists():
        return HttpResponseForbidden("Você não tem permissão para reservar quartos.")

    if not q.status:
        return HttpResponseForbidden("Este quarto já está reservado.")

    nome = ''
    telefone = ''

    if request.method == "POST":
        nome = request.POST.get('nome_cliente')
        telefone = request.POST.get('telefone_cliente')

        Reserva.objects.create(quarto=q, nome_cliente=nome, telefone_cliente=telefone)
        q.status = False
        q.save()
        return redirect('quartos')

    return render(request, 'reserva.html', {
        'quarto': q,
        'nome_cliente': nome,
        'telefone_cliente': telefone
    })


@login_required(login_url='/')
def liberar_quarto(request, quarto_id):
    user = request.user
    q = get_object_or_404(quarto, id=quarto_id)

    if not user.groups.filter(name__in=['Gerente', 'Colaborador']).exists():
        return HttpResponseForbidden("Você não tem permissão para liberar quartos.")

    Reserva.objects.filter(quarto=q).delete()
    q.status = True
    q.save()

    return redirect('quartos')

@user_passes_test(is_gerente, login_url='/')
def editar_quarto(request, quarto_id):
    q = get_object_or_404(quarto, id=quarto_id)

    if request.method == "POST":
        form = quartoForms(request.POST, request.FILES, instance=q)
        if form.is_valid():
            form.save()
            return redirect('quartos')
    else:
        form = quartoForms(instance=q)
    
    return render(request, 'editar_quarto.html', {'form': form, 'quarto': q})


def excluir_quarto(request, quarto_id):
    if not request.user.groups.filter(name="Gerente").exists():
        return HttpResponseForbidden("Apenas gerentes podem excluir quartos.")
    
    q = get_object_or_404(quarto, id=quarto_id)
    q.delete()
    return redirect('quartos')