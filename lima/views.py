from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .models import Pessoa, Amostra, Label
import numpy as np
import random


def get_random_filenames(n,pessoa):
    print("Id:",pessoa)
    labeled_files = Label.objects.values_list('amostra_id',flat= True).filter(pessoa_id=pessoa)
    unique_labeled= np.unique(labeled_files).tolist()
    print("Classificadas:",unique_labeled)
    lista_amostras=list(Amostra.objects.values_list('id',flat=True))
    print("Amostras:",lista_amostras)
    for a in unique_labeled:
        if a in lista_amostras:
            lista_amostras.remove(a)
    if len(lista_amostras)<=n:
        n=len(lista_amostras)
    randomList = random.sample(lista_amostras, n)
    print("Lista de amostras final:",lista_amostras)
    print("Lista escolhida:", randomList)
    filenames = Amostra.objects.values_list('amostra', flat=True).filter(id__in= randomList)
    dict_amostra = list(Amostra.objects.values('id','amostra').filter(id__in=randomList))
    return filenames,dict_amostra


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
        filenames,dict_amostra = get_random_filenames(10,request.session['id_pessoa'])
        print(dict_amostra)
        if dict_amostra:
                request.session['dict_amostra'] = dict_amostra
                return render(request, 'classificar.html', {'amostras': filenames, 'primeiro': primeiro})
        else:
            return render(request, 'agradecimento.html')
    else:
        print("Preciso de um email")
        message = 'email'
        return render(request, 'index.html',{'message': message})


def registrar(request):
    message=''
    primeiro = False
    idpessoa=request.session.get('id_pessoa')
    dict_amostra=request.session.get('dict_amostra')
    print(dict_amostra)
    for aux in range(len(dict_amostra)):
        nome=dict_amostra[aux].get('amostra')
        print("Nome",nome)
        label=(request.POST.get(nome))
        print(request.POST)
        print("Label",label)
        if label is None:
            print("Me classifica! Esqueceu de mim ...", nome, label)
            message="amostra"
        else:
            idamostra= dict_amostra[aux].get('id')
            print(label[0],label[1],dict_amostra[aux].get('id'),idpessoa)
            info_label=Label(maturacao=label[0],defeito=label[1],amostra=Amostra.objects.get(id=idamostra),pessoa=Pessoa.objects.get(id=idpessoa))
            info_label.save()
            print("Salvei")
    if 'finalizar' in request.POST:
        return render(request, 'agradecimento.html')
    elif 'mais' in request.POST:
        filenames_novos, dict_amostra_novo = get_random_filenames(8,request.session['id_pessoa'])
        print(dict_amostra_novo)
        if dict_amostra_novo :
                request.session['dict_amostra'] = dict_amostra_novo
                return render(request, 'classificar.html', {'amostras': filenames_novos, 'primeiro': primeiro,'message': message})
        else:
            return render(request, 'agradecimento.html')