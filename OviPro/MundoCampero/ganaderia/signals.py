# signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Raza, CalificadorPureza


@receiver(post_migrate)
def cargar_datos_iniciales(sender, **kwargs):
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
            Raza.objects.get_or_create(nombre=raza)
        
        calificadores = ['pedigri','PO','MO','general']
        for calificador in calificadores:
            CalificadorPureza.objects.get_or_create(nombre=calificador)
        

