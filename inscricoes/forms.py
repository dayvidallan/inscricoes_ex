from django import forms

from .models import Inscricao, FimInscricoes


class InscricaoForm(forms.ModelForm):

    class Meta:
        model = Inscricao
        fields = 'nome','cpf', 'email', 'telefone', 'endereco', 'numero', 'cidade', 'estado', 'cep', 'data_nascimento', 'upload',


class InscricaoNotaForm(forms.ModelForm):

    class Meta:
        model = Inscricao
        fields = 'nome','cpf', 'email', 'telefone', 'endereco', 'numero', 'cidade', 'estado', 'cep', 'data_nascimento', 'nota', 'upload',


class DocumentoForm(forms.ModelForm):

    class Meta:
        model = Inscricao
        fields = 'upload',


class AvisoForm(forms.ModelForm):

    class Meta:
        model = FimInscricoes
        fields = 'aviso','fim_inscricao',


