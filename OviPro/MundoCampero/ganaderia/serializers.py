# serializers.py
from rest_framework import serializers
from .models import Oveja


class OvejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oveja
        fields = [
            'BU',
            'RP',
            'nombre',
            'peso',
            'raza',
            'edad',
            'fecha_nacimiento',
            'sexo',
            'calificador_pureza',
            'observaciones',
            'oveja_padre',
            'oveja_madre',
            'establecimiento',
            'estado',
            'rp_padre_externo',
            'rp_madre_externo',
            ]
    