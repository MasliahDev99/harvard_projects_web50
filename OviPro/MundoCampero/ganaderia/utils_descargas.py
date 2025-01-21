"""
This module handles the generation and download of records in various formats (XLSX, CSV) for ovine and sales data. 

Responsibilities:
- Converts data into XLSX or CSV format for records related to ovine and sales management.
- Saves the generated files in the media folder and serves them for download.
- Fetches data from the database models (`Oveja`, `Venta`) for record generation.
- Ensures flexibility in exporting data for different requirements and use cases.

Dependencies:
- Pandas: For creating XLSX files.
- CSV module: For generating CSV files.
- Django: To interact with models and manage HTTP responses.
"""

import os
import pdfkit
import pandas as pd
import csv 
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
from .models import Oveja, Venta

# Configure the media path where files will be saved
MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL

def convertir_formato_xlsx(contenido, nombre_archivo):
    """
    Converts data into XLSX format and saves it in the media folder.

    Args:
        contenido (list of dict): The data to convert into XLSX format.
        nombre_archivo (str): The name of the output file (without extension).

    Returns:
        str: The path to the saved XLSX file.
    """
    df = pd.DataFrame(contenido)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Contenido')
        writer.close()  # Ensure data is written correctly

    output.seek(0)

    # Define the path to save the file in the media folder
    path = os.path.join(MEDIA_ROOT, f'{nombre_archivo}.xlsx')
    with open(path, 'wb') as f:
        f.write(output.read())

    return path

def generar_csv(nombre_archivo: str, datos: list, campos: list = ['BU', 'RP', 'nombre', 'peso(kg)', 'raza', 'edad(meses)', 'sexo', 'calificador_pureza', 'estado','Lugar_origen']):
    """
    Generates and saves a CSV file in the media folder.

    Args:
        nombre_archivo (str): The name of the file (without extension).
        datos (list): A list of dictionaries containing the data for the CSV.
        campos (list): A list of column names for the CSV file.

    Returns:
        str: The path to the saved CSV file.
    """
    path = os.path.join(MEDIA_ROOT, f'{nombre_archivo}.csv')

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()  # Write column headers
        for fila in datos:
            writer.writerow(fila)  # Write each row of data

    return path

def obtener_contenido_registro(establecimiento, tipo_registro: str = 'registro_ovino'):
    """
    Fetches the content for the specified record type (ovine or sales records).

    Args:
        establecimiento: The establishment from which to fetch the records.
        tipo_registro: The type of record ('registro_ovino' or 'registro_venta').

    Returns:
        list or dict: The content for the specified record type.
    """
    ovinos = Oveja.objects.filter(establecimiento=establecimiento, estado='activa')

    if tipo_registro not in ['registro_ovino', 'registro_venta']:
        raise ValueError(f"Invalid record type: {tipo_registro}")

    if tipo_registro == 'registro_ovino':
        if not ovinos:
            return {'message': 'No active ovinos found for this establishment.'}
        contenido = [{
            'RP': ovino.RP if ovino.RP else None,
            'BU': ovino.BU if ovino.BU else None,
            'nombre': ovino.nombre,
            'peso(kg)': ovino.peso,
            'raza': ovino.raza,
            'edad(meses)': ovino.edad,
            'sexo': ovino.sexo,
            'calificador_pureza': ovino.calificador_pureza,
            'estado': ovino.estado,
            'Lugar_origen': ovino.establecimiento_origen if ovino.establecimiento_origen else ovino.establecimiento.username,
        } for ovino in ovinos]

    else:
        ventas = Venta.objects.filter(establecimiento=establecimiento)
        if not ventas:
            return {'message': 'No sales records found for this establishment.'}
        contenido = [
            {
                'fecha_venta': venta.fecha_venta,
                'tipo_venta': venta.tipo_venta,
                'peso_total(kg)': venta.peso_total,
                'valor_carne(US$/kg)': venta.valor_carne,
                'valor(US$)': venta.valor,
                'ovejas': [oveja.nombre for oveja in venta.ovejas.all()]
            } for venta in ventas
        ]

    return contenido

def descargar_registro(establecimiento, tipo_registro: str = 'registro_ovino', nombre_archivo: str = 'tabla_ovinos', extension: str = '.xlsx'):
    """
    Generates and saves a file in the specified format based on the record type.

    Args:
        establecimiento: The establishment to fetch data for.
        tipo_registro (str): Type of record ('registro_ovino', 'registro_venta').
        nombre_archivo (str): Name of the output file (without extension).
        extension (str): File format for the download ('.xlsx', '.csv').

    Returns:
        HttpResponse: Response with the requested file ready for download.
    """
    contenido = obtener_contenido_registro(establecimiento=establecimiento, tipo_registro=tipo_registro)

    if extension == '.xlsx':
        ruta_archivo = convertir_formato_xlsx(contenido=contenido, nombre_archivo=nombre_archivo)
    elif extension == '.csv':
        ruta_archivo = generar_csv(nombre_archivo=nombre_archivo, datos=contenido)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    # Serve the saved file from the /media/ folder
    with open(ruta_archivo, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(ruta_archivo)}'

    return response