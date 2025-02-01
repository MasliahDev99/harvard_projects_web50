from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Raza, CalificadorPureza, Oveja, Venta
from django.contrib.admin.views.main import ChangeList
from .forms.venta_forms import VentaForm

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'RUT', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'RUT')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('RUT',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('RUT',)}),
    )

@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Changed 'nombre' to 'name'
    search_fields = ('name',)      # Changed 'nombre' to 'name'
    ordering = ('name',)           # Changed 'nombre' to 'name'
    list_per_page = 25

@admin.register(CalificadorPureza)
class CalificadorPurezaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Changed 'nombre' to 'name'
    search_fields = ('name',)      # Changed 'nombre' to 'name'
    ordering = ('name',)           # Changed 'nombre' to 'name'
    list_per_page = 25

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    form = VentaForm
    list_display = ('id', 'sale_date', 'establishment', 'sale_type', 'valor_total_display', 'ovejas_asociadas')  # Changed field names
    list_filter = ('sale_type', 'sale_date', 'establishment')  # Changed field names
    search_fields = ('id', 'ovejas__name', 'establishment__name')  # Changed 'nombre' to 'name'
    ordering = ('-sale_date',)  # Changed 'fecha_venta' to 'sale_date'

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



# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Oveja)