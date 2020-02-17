# encoding:utf-8
from django import forms
from clientes.models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Identificación', 'size': '10'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres', 'size': '60'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos', 'size': '100'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Direccion', 'size': '100'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono', 'size': '20'}),
        }

    def clean_identificacion(self):
        diccionario_limpio = self.cleaned_data
        identificacion = diccionario_limpio.get('identificacion')
        if len(identificacion) < 10 or len(identificacion) > 10:
            raise forms.ValidationError("Debe tener 10 digitos")
        return identificacion

    def clean_nombres(self):
        nombre = self.cleaned_data['nombres']
        if not nombre.isalpha():
            raise forms.ValidationError('No puede contener números')
        return nombre
