from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Raza, CalificadorPureza, Oveja,Venta
from django.contrib.admin.views.main import ChangeList
from .forms.venta_forms import VentaForm 

# Configuración personalizada para el modelo de Usuario
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


@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Campos visibles en la lista
    search_fields = ('nombre',)     # Campos para buscar
    ordering = ('nombre',)          # Ordenar por nombre
    list_per_page = 25              # Paginación en la lista


@admin.register(CalificadorPureza)
class CalificadorPurezaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 25


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    form = VentaForm
    
    list_display = ('id', 'fecha_venta', 'establecimiento', 'tipo_venta', 'valor_total_display', 'ovejas_asociadas')
    list_filter = ('tipo_venta', 'fecha_venta', 'establecimiento')
    search_fields = ('id', 'ovejas__nombre', 'establecimiento__nombre')
    ordering = ('-fecha_venta',)

    def valor_total_display(self, obj):
        return f"${obj.valor:.2f}" if obj.valor else "-"
    valor_total_display.short_description = "Valor Total"

    def ovejas_asociadas(self, obj):
        return ", ".join([str(oveja.RP) for oveja in obj.ovejas.all()])
    ovejas_asociadas.short_description = "Ovejas"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form


# Registrar los modelos en el admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Oveja)  # Si Oveja también necesita configuración personalizada, puedes agregar una clase Admin aquí
