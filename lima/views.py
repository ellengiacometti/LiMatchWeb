from django.shortcuts import render
from django.http import HttpResponse
from .models import Pessoa, Amostra
import random

def get_random_filenames(n):
    max_id = Amostra.objects.latest('id').id
    randomList = random.sample(range(1, max_id), n)
    filenames = Amostra.objects.values_list('amostra', flat=True).filter(id__in= randomList)
    return filenames

# Create your views here.

def index(request):

    return render(request, 'index.html')



def classificar(request):
    # TODO: TRATAMENTO PESSOA VAZIA
    primeiro = True
    email = request.POST["email"]
    if email:
        email_cadastrado = Pessoa.objects.filter(email=email).count()
        if email_cadastrado == 0:
            cargo = request.POST["cargo"]
            nome = request.POST["name"]
            info_pessoa = Pessoa(nome=nome, email=email, cargo=cargo)
            info_pessoa.save()
            print("inseriu!")
        request.session['id_pessoa']=Pessoa.objects.get(email=email).pk
        filenames = get_random_filenames(2)
        return render(request, 'classificar.html', {'amostras': filenames, 'primeiro': primeiro})
    else:
        print("Preciso de um email")
        return render(request, 'index.html')


def registrar(request):
    primeiro = False
    idpessoa=request.session.get('id_pessoa')

    print(idpessoa)
    if 'finalizar' in request.POST:
        return render(request, 'agradecimento.html')
    elif 'mais' in request.POST:
        filenames = get_random_filenames(4)
        return render(request, 'classificar.html', {'amostras': filenames, 'primeiro': primeiro})
