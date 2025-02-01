# signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Raza, CalificadorPureza


@receiver(post_migrate)
def cargar_datos_iniciales(sender, **kwargs):
    """
    This signal is triggered after the database migration has been completed.
    
    The `post_migrate` signal is used to perform post-migration tasks, such as 
    loading initial data into the database, ensuring that certain essential records 
    exist after the migrations are applied. In this case, after running the migrations 
    for the 'ganaderia' app, we populate the `Raza` and `CalificadorPureza` models 
    with predefined lists of data, if they do not already exist.

    This approach is useful to automate the population of essential data without
    requiring manual entry or a custom data import script. It ensures that the 
    database is seeded with basic values as part of the migration process, making
    it easier for developers and administrators to get started with the system.

    Steps performed:
    1. Load predefined sheep breeds into the `Raza` model.
    2. Load predefined purity qualifiers into the `CalificadorPureza` model.
    
    Args:
        sender: The model class that triggered the signal. In this case, it's the 
                'ganaderia' app's migration process.
        **kwargs: Additional keyword arguments provided by the signal framework. 
                  These can be used for additional logic or debugging.
    """
    # Luego de hacer las migraciones iniciales , se cargaran las razas y calificadores de pureza automaticamente
    if sender.name == 'ganaderia':
        # cargamos las razas de ovinos 
        razas = [
                'Texel',
                'Merino',
                'Corriedale',
                'Criolla',
                'Dohne Merino',
                'Dorper',
                'Finnish Landrace',
                'Frisona Milchschaf',
                'Hampshire Down',
                'Highlander',
                'Ideal',
                'Ile de France',
                'Merilin',
                'Merino Australiano',
                'Poll Dorset',
                'Romney Marsh',
                'SAMM',
                'Southdown',
                'Suffolk'
                ]
        for raza in razas:
            Raza.objects.get_or_create(name=raza)
        
        calificadores = ['pedigri','PO','MO','general']
        for calificador in calificadores:
            CalificadorPureza.objects.get_or_create(name=calificador)
        


        

