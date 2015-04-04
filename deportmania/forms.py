__author__ = 'Alejandro'
from django.forms import ModelForm
from django import forms
from deportmania.models import *
from django.contrib.auth.models import User


class userDjangoForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class DeporUserRegistrationForm(ModelForm):
    class Meta:
        model = DeporUser
        fields = ('birthday', 'gender', 'poblacion')


class FamiliaForm(ModelForm):
    class Meta:
        model= Familia
        fields=('nombre','pesomedio')


class ProveedorForm(ModelForm):
    class Meta:
        model=Proveedor
        fields=('nombre','direccion','contacto')

class CompaniaForm(ModelForm):
    class Meta:
        model=Compania
        fields=('preciopeso1','preciopeso2','preciopeso3','gastoextra','nombre','contacto')


class SearchUserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)

class SearchArticulo(forms.Form):
    filter = forms.CharField(label='', max_length=100)