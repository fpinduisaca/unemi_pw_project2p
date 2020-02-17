# encoding:utf-8
from django import forms
from .models import Medicamentos, Presentacion


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamentos
        fields = '__all__'
        widgets = {
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'id': 'valor3'}),
            'presentacion': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_expiracion': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'Date', 'data-date-format': 'dd/mm/yyyy'}),
            'fecha_produccion': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'Date1', 'data-date-format': 'dd/mm/yyyy'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control', 'id': 'iva'}),
        }


class CrearmedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamentos
        fields = '__all__'
        widgets = {
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'id': 'precio_compra'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'id': 'precio_venta'}),
            'presentacion': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_expiracion': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'Date', 'data-date-format': 'dd/mm/yyyy'}),
            'fecha_produccion': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'Date1', 'data-date-format': 'dd/mm/yyyy'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control', 'id': 'iva'}),
        }


class CrearpresentacionForm(forms.ModelForm):
    class Meta:
        model = Presentacion
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
