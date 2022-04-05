from django import forms

from .models import Inscricao


class InscricaoForm(forms.ModelForm):

    class Meta:
        model = Inscricao
        fields = 'nome','cpf', 'email', 'telefone', 'endereco', 'numero', 'cidade', 'estado', 'cep', 'data_nascimento', 'upload',

class DocumentoForm(forms.ModelForm):

    class Meta:
        model = Inscricao
        fields = 'upload',

