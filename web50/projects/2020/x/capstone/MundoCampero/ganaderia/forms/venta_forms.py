# forms/venta_forms.py
from django import forms
from ..models import Venta,Oveja
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class VentaForm(ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener el tipo de venta del POST data o del objeto existente
        data = kwargs.get('data', {})
        instance = kwargs.get('instance')
        tipo_venta = data.get('tipo_venta') if data else (instance.tipo_venta if instance else None)

        # Configurar campos según el tipo de venta
        if tipo_venta == 'frigorifico':
            self.fields['peso_total'] = forms.DecimalField(
                required=True,
                label='Peso Total (kg)',
                widget=forms.NumberInput(attrs={'step': '0.01'})
            )
            self.fields['valor_carne'] = forms.DecimalField(
                required=True,
                label='Valor por kg',
                widget=forms.NumberInput(attrs={'step': '0.01'})
            )
        elif tipo_venta == 'remate':
            if 'peso_total' in self.fields:
                del self.fields['peso_total']
            if 'valor_carne' in self.fields:
                del self.fields['valor_carne']
            self.fields['valor'].required = True
        elif tipo_venta == 'individual':
            if 'peso_total' in self.fields:
                del self.fields['peso_total']
            if 'valor_carne' in self.fields:
                del self.fields['valor_carne']
            self.fields['valor'].required = True
        elif tipo_venta == 'donacion':
            if 'peso_total' in self.fields:
                del self.fields['peso_total']
            if 'valor_carne' in self.fields:
                del self.fields['valor_carne']
            self.fields['valor'].initial = 0
            self.fields['valor'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        tipo_venta = cleaned_data.get('tipo_venta')
        
        if tipo_venta == 'frigorifico':
            peso_total = cleaned_data.get('peso_total')
            valor_carne = cleaned_data.get('valor_carne')
            if not peso_total or not valor_carne:
                raise ValidationError('Para ventas a frigorífico, debe especificar peso total y valor por kg')
            # Calcular el valor total
            cleaned_data['valor'] = peso_total * valor_carne
        
        return cleaned_data