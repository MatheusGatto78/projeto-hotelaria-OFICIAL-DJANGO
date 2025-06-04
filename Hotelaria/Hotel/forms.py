from django import forms
from .models import quarto
from django.contrib.auth.models import User


class quartoForms(forms.ModelForm):
    class Meta:
        model = quarto
        fields = [ 'num_quarto', 'qnt_hospedes', 'tipo', 'valor', 'descricao', 'status','img']

class ColaboradorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']