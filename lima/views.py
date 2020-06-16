from django.shortcuts import render
from django.http import HttpResponse
from .models import Pessoa, Amostra, Label
import random

def get_random_filenames(n):
    max_id = Amostra.objects.latest('id').id
    randomList = random.sample(range(1, max_id), n)
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
        filenames,dict_amostra = get_random_filenames(2)
        request.session['dict_amostra'] = dict_amostra
        return render(request, 'classificar.html', {'amostras': filenames, 'primeiro': primeiro})
    else:
        print("Preciso de um email")
        return render(request, 'index.html')


def registrar(request):
    primeiro = False
    idpessoa=request.session.get('id_pessoa')
    dict_amostra=request.session.get('dict_amostra')
    for aux in range(len(dict_amostra)):
          label=(request.POST.get(dict_amostra[aux].get('amostra')))
          if label is None:
              print("Esqueceu de preencher!")
          else:
              print(label[0],label[1],dict_amostra[aux].get('id'),idpessoa)
              info_label=Label(maturacao=label[0],defeito=label[1],amostra_id=dict_amostra[aux].get('id'),pessoa_id=idpessoa)
              info_label.save()
              print("Salvei")
                # print(dict_amostra[aux].get('id'),dict_amostra[aux].get('amostra'))
    if 'finalizar' in request.POST:
        return render(request, 'agradecimento.html')
    elif 'mais' in request.POST:
        filenames_novos, dict_amostra_novo = get_random_filenames(4)
        request.session['dict_amostra'] = dict_amostra_novo
        return render(request, 'classificar.html', {'amostras': filenames_novos, 'primeiro': primeiro})
