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
    # amostras=[]

    # for id_amostra in ids_amostra:
    #       amostras.append(Amostra.objects.get(id=id_amostra))
    #       print(amostras)
    filenames=get_random_filenames(9)
    return render(request, 'index.html',{'amostras':filenames})


def teste(request):
    # TODO: TRATAMENTO PESSOA VAZIA
    email = request.POST["email"]
    if email:
        email_cadastrado = Pessoa.objects.filter(email=email).count()
        if email_cadastrado == 0:
            cargo = request.POST["cargo"]
            nome = request.POST["name"]
            info_pessoa = Pessoa(nome=nome, email=email, cargo=cargo)
            info_pessoa.save()
    else:
        print("Preciso de um email")

    return render(request,'index.html')
