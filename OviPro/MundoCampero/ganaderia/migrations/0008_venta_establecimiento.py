# Generated by Django 4.2.17 on 2025-01-03 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ganaderia', '0007_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='establecimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to=settings.AUTH_USER_MODEL),
        ),
    ]
