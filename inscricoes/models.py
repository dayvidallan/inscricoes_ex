from django.db import models
from django.urls import reverse_lazy




class Inscricao(models.Model):
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField()
    cpf = models.CharField(u'CPF', max_length=20)
    telefone = models.CharField(max_length=100, unique=False)
    endereco = models.CharField(max_length=100, unique=False)
    numero = models.DecimalField('numero', max_digits=7, decimal_places=2)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField('cep', max_length=10, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    nota = models.DecimalField(u'Valor Médio', max_digits=20, decimal_places=2, null=True, blank=True)
    upload = models.FileField(upload_to='upload', null=True, blank=True)


    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse_lazy('inscricoes:produto_detail', kwargs={'pk': self.pk})

