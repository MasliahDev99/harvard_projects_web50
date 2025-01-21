import weasyprint
import pdfkit
import pandas as pd
import os
from io import BytesIO
from django.http import HttpResponse


# descarga de archivos en formato pdf
# archivos -> registro de los ovinos y ventas en formato de tabla como .xls o .pdf

def convertir_formato_xls(archivo):
    """
        Convierte un archivo a formato xls
    """
    pass

def convertir_formato_pdf(archivo):
    """
        Convierte un archivo a formato pdf
    
    """
    pass

def descargar_registro(tipo_registro:str='registro_ovino',nombre_archivo:str='tabla_ovinos',extensiones:list=['.xls','.pdf']):
    """
        Dado un tipo de registro (registro_ovino, registro_ventas) nombre del fichero , extension [xls,pdf] y directorio destino
        genera un archivo con el contenido de las tablas y se guarda en la carpeta de descarga del equipo del cliente
    """
    pass
