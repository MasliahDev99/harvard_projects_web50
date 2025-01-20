# serializers.py
from rest_framework import serializers
from .models import Oveja,Venta,User
from .utils import obtener_todos_tipos_cantidad,informacion_de_ventas


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
            'padre',
            'madre',
            'establecimiento',
            'estado',
            'establecimiento_origen',
            ]
    
class VentaSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Venta
        fields = [
            'ovejas',
            'fecha_venta',
            'peso_total',
            'valor_carne',
            'establecimiento',
            'tipo_venta',
            ]
        
class EstablecimientoSerializer(serializers.ModelSerializer):
    cantidad_ovinos = serializers.SerializerMethodField()
    cantidad_ventas_cat = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'RUT',
            'fecha_registro',
            'registro_ARU_criador',

            # cantidad de ovinos y ventas
            'cantidad_ovinos',
            'cantidad_ventas_cat',
        ]
    
    def get_cantidad_ovinos(self, obj):
       
        corderos, corderas, borregos, borregas, carneros, ovejas, total_ovejas = obtener_todos_tipos_cantidad(self.context['request'])

        # Devolvemos el diccionario con la cantidad de ovinos
        return {
            'Corderos': corderos,
            'Corderas': corderas,
            'Borregos': borregos,
            'Borregas': borregas,
            'Carneros': carneros,
            'Ovejas': ovejas,
            'Total Ovejas': total_ovejas
        }
    
    def get_cantidad_ventas_cat(self, obj):
       
        ventas_info = informacion_de_ventas(self.context['request'])

        # Retornamos el diccionario con la cantidad de ventas por categoría
        return {
            'cantidad_ventas_por_remate': ventas_info['cantidad_ventas_por_remate'],
            'cantidad_ventas_por_frigorifico': ventas_info['cantidad_ventas_por_frigorifico'],
            'cantidad_ventas_por_individual': ventas_info['cantidad_ventas_por_individual'],
            'cantidad_donaciones': ventas_info['cantidad_donaciones'],
        }

    

    