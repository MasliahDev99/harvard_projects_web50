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
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
from .models import Oveja, Venta

# Configure the media path where files will be saved
MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL


#Determine the Downloads directory path
def get_downloads_path():
    """
        Determines the path to the Downloads directory.
        return:
            str: The path to the Downloads directory.
    """
    home = Path.home()
    possible_dirs = ['Downloads','Descargas'] #Add more localized name if needed
    for dir_name in possible_dirs:
        downloads_path = home / dir_name
        if downloads_path.exists():
            return downloads_path
    return home

DOWNLOADS_DIR = get_downloads_path()


def format_to_xlsx(content, filename):
    """
    Converts data into XLSX format and saves it in the media folder.

    Args:
        content (list of dict): The data to convert into XLSX format.
        filename (str): The name of the output file (without extension).

    Returns:
        str: The path to the saved XLSX file.
    """
    df = pd.DataFrame(content)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Content')
        writer.close()  # Ensure data is written correctly

    output.seek(0)

    # Define the path to save the file in the media folder
    path = os.path.join(DOWNLOADS_DIR, f'{filename}.xlsx')
    with open(path, 'wb') as f:
        f.write(output.read())

    return path

def generate_csv(filename: str, data: list, fields: list = ['BU', 'RP', 'name', 'weight(kg)', 'breed', 'age(months)', 'sex', 'purity_qualifier', 'status', 'origin_place']):
    """
    Generates and saves a CSV file in the media folder.

    Args:
        filename (str): The name of the file (without extension).
        data (list): A list of dictionaries containing the data for the CSV.
        fields (list): A list of column names for the CSV file.

    Returns:
        str: The path to the saved CSV file.
    """
    path = os.path.join(MEDIA_ROOT, f'{filename}.csv')

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()  # Write column headers
        for row in data:
            writer.writerow(row)  # Write each row of data

    return path

def get_register_content(establishment, register_type: str = 'ovine_record'):
    """
    Fetches the content for the specified record type (ovine or sales records).

    Args:
        establishment: The establishment from which to fetch the records.
        register_type: The type of record ('ovine_record' or 'sales_record').

    Returns:
        list or dict: The content for the specified record type.
    """
    active_sheep = Oveja.objects.filter(establishment=establishment, status='active')

    if register_type not in ['ovine_record', 'sales_record']:
        raise ValueError(f"Invalid record type: {register_type}")

    if register_type == 'ovine_record':
        if not active_sheep:
            return {'message': 'No active sheep found for this establishment.'}
        content = [{
            'RP': sheep.RP if sheep.RP else None,
            'BU': sheep.BU if sheep.BU else None,
            'name': sheep.name,
            'weight(kg)': sheep.weight,
            'breed': sheep.raza.name,
            'age(months)': sheep.age,
            'sex': sheep.sex,
            'purity_qualifier': sheep.purity_qualifier.name,
            'status': sheep.status,
            'origin_place': sheep.origin_establishment if sheep.origin_establishment else sheep.establishment.username,
        } for sheep in active_sheep]

    else:
        sales = Venta.objects.filter(establishment=establishment)
        if not sales:
            return {'message': 'No sales records found for this establishment.'}
        content = [
            {
                'sale_date': sale.sale_date,
                'sale_type': sale.sale_type,
                'total_weight(kg)': sale.total_weight,
                'meat_value(US$/kg)': sale.meat_value,
                'value(US$)': sale.value,
                'sheep': [sheep.name for sheep in sale.sheep.all()]
            } for sale in sales
        ]

    return content

def download_register(establishment, register_type: str = 'ovine_record', filename: str = 'sheep_table', extension: str = '.xlsx'):
    """
    Generates and saves a file in the specified format based on the record type.

    Args:
        establishment: The establishment to fetch data for.
        register_type (str): Type of record ('ovine_record', 'sales_record').
        filename (str): Name of the output file (without extension).
        extension (str): File format for the download ('.xlsx', '.csv').

    Returns:
        HttpResponse: Response with the requested file ready for download.
    """
    content = get_register_content(establishment=establishment, register_type=register_type)

    if extension == '.xlsx':
        path = format_to_xlsx(content=content, filename=filename)
    elif extension == '.csv':
        path = generate_csv(filename=filename, data=content)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    # Serve the saved file from the /media/ folder
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(path)}'

    return response