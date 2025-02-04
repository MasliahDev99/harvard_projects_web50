#signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def initialize_default_categories(sender,**kwargs):
    categories = [
        'Electronics',
        'Fashion',
        'Home & Garden',
        'Toys & Games',
        'Books & Movies',
        'Health & Beauty',
        'Sports & Outdoors',
        'Automotive',
        'Collectibles',
        'Vehicles',
        'Other',
        ]
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)