from django.db import models
from django.utils.timezone import now

# Create your models here.
class Pessoa(models.Model):
    CARGOS = [('ET', 'Estudante'), ('PF', 'Professor'), ('TI', 'TI'), ('OT', 'Outros')]
    nome = models.CharField(max_length=200)
    email = models.CharField(max_length=200,unique=True)
    cargo = models.CharField(max_length=2, choices=CARGOS, default='OT')

    def __str__(self):
        return self.email


class Amostra(models.Model):
    TIPOS = [('ORIGINAL', 'Original'), ('DA', 'DataAugmentation'), ('CDV', 'CrossDataset')]
    BASES=[('TS','TESTE'),('TR','TREINO')]
    amostra = models.CharField(max_length=200, unique=True)
    data_amostra = models.DateField(default=now)
    base=models.CharField(max_length=10, choices=BASES, default='TR')
    tipo = models.CharField(max_length=10, choices=TIPOS, default='ORIGINAL')
    kurtosis = models.FloatField(default=None)
    skewness= models.FloatField(default=None)
    dissimilarity= models.FloatField(default=None)
    correlation= models.FloatField(default=None)
    homogeneity= models.FloatField(default=None)
    energy= models.FloatField(default=None)
    contrast= models.FloatField(default=None)
    asm= models.FloatField(default=None)
    color=models.TextField(max_length=600)
    raio= models.FloatField(default=None)

    def __str__(self):
        return self.amostra


class Label(models.Model):
    amostra = models.ForeignKey(Amostra, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(default=now)
    maturacao = models.CharField(max_length=1)
    defeito = models.CharField(max_length=1)

    def __str__(self):
        return self.amostra,self.email,self.datahora

