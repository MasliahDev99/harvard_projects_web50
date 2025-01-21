# serializers.py
from rest_framework import serializers
from .models import Oveja,Venta,User
from .utils import obtener_todos_tipos_cantidad,informacion_de_ventas

"""
This module contains serializers for the 'Oveja' (Sheep), 'Venta' (Sale), and 'Establecimiento' (Establishment) models.
The purpose of these serializers is to transform the model instances into JSON format, allowing dynamic data to be 
sent from the server to the frontend for display in the dashboard and analysis views.

1. `OvejaSerializer`: Serializes data related to sheep. It includes details like RP (Registration Number), weight, breed, 
   age, and observations. This serializer is useful when displaying specific sheep information in the frontend.
   
2. `VentaSerializer`: Serializes data related to sales. It includes details like the sheep involved in the sale, total weight, 
   value of the meat, and the type of sale. This serializer is used to send information about sheep sales to the frontend.
   
3. `EstablecimientoSerializer`: Serializes data related to the establishment (the user). It includes additional fields that calculate 
   the total number of sheep and sales per category dynamically using custom methods. This serializer is useful for showing 
   an overview of the establishment’s data, such as the total number of sheep of different types and the number of sales 
   categorized by type (remate, frigorífico, individual sales, and donations).

### Key Features:
- `cantidad_ovinos`: A dynamic field that calculates the number of sheep by type (e.g., lambs, ewes, rams, etc.) for the 
  establishment, using the `obtener_todos_tipos_cantidad` function.
  
- `cantidad_ventas_cat`: A dynamic field that calculates the number of sales per category (e.g., auction, slaughterhouse, 
  individual sales, donations) using the `informacion_de_ventas` function.

### Purpose:
These serializers are used to send dynamic data from the backend to the frontend, where it can be visualized in the dashboard 
or used for further analysis. The data sent includes the count of sheep by type and the number of sales per category, making 
it easier for users to understand the distribution of sheep and sales within the establishment.

### Integration:
This module works as part of the API that provides dynamic data for the frontend, particularly for the dashboard and analysis 
pages. The frontend can consume the API responses to display the data in real-time, providing users with valuable insights 
about their sheep and sales activity.

Example API Endpoints:
- `/api/ovejas/` - List of sheep with all their details.
- `/api/ventas/` - List of sales with related sheep data.
- `/api/establecimiento/` - Information about the establishment, including the number of sheep and sales.

By using these serializers, the backend can send structured data to the frontend in a consistent manner, ensuring that 
users can visualize key metrics related to their establishment in real-time.
"""

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

    

    