from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Definir los campos que aparecerán en la lista de usuarios
    list_display = ('username', 'email', 'RUT', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'RUT')

    # Definir los campos que aparecerán al editar el usuario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('RUT',)}),
    )

    # Campos en el formulario de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('RUT',)}),
    )

    

# Registrar el modelo de usuario con el admin personalizado
admin.site.register(User, CustomUserAdmin)