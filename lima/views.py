from django.shortcuts import render
from django.http import HttpResponse
from .models import Pessoa


# Create your views here.
def index(request):
    print(request.method)
    return render(request, 'index.html')


def teste(request):
    email=request.POST["email"]
    email_cadastrado = Pessoa.objects.filter(email=email).count()

    if email_cadastrado == 0 :
        cargo = request.POST["cargo"]
        nome = request.POST["name"]
        info_pessoa=Pessoa(nome=nome,email=email,cargo=cargo)
        info_pessoa.save()
    return render(request,'index.html')
