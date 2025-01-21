from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Raza, CalificadorPureza, Oveja,Venta
from django.contrib.admin.views.main import ChangeList
from .forms.venta_forms import VentaForm 

# Configuración personalizada para el modelo de Usuario
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model to display additional fields 
    and customize user management within the Django admin interface.

    Attributes:
        list_display (tuple): Defines the columns to display in the user list view.
        search_fields (tuple): Defines which fields to search for when filtering users.
        fieldsets (tuple): Defines the fields to display when editing a user.
        add_fieldsets (tuple): Defines the fields to display when adding a new user.
    """
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
    """
    Admin configuration for the Raza model, which represents sheep breeds.

    Attributes:
        list_display (tuple): Defines the columns to display in the breed list view.
        search_fields (tuple): Defines which fields to search for when filtering breeds.
        ordering (tuple): Defines the default ordering for the breed list view.
        list_per_page (int): Defines the number of breeds displayed per page.
    """
    list_display = ('id', 'nombre')  # Campos visibles en la lista
    search_fields = ('nombre',)     # Campos para buscar
    ordering = ('nombre',)          # Ordenar por nombre
    list_per_page = 25              # Paginación en la lista


@admin.register(CalificadorPureza)
class CalificadorPurezaAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CalificadorPureza model, which represents purity 
    classifiers for sheep.

    Attributes:
        list_display (tuple): Defines the columns to display in the purity classifier list view.
        search_fields (tuple): Defines which fields to search for when filtering purity classifiers.
        ordering (tuple): Defines the default ordering for the purity classifier list view.
        list_per_page (int): Defines the number of purity classifiers displayed per page.
    """
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 25


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Venta (Sale) model, used to manage sheep sales.

    Attributes:
        form (ModelForm): Custom form used to validate and display data when adding/editing sales.
        list_display (tuple): Defines the columns to display in the sales list view.
        list_filter (tuple): Defines the filters available in the sales list view.
        search_fields (tuple): Defines which fields to search for when filtering sales.
        ordering (tuple): Defines the default ordering for the sales list view.
        valor_total_display (method): Displays the total value of the sale formatted as currency.
        ovejas_asociadas (method): Displays a comma-separated list of sheep associated with the sale.
    """
    form = VentaForm
    
    list_display = ('id', 'fecha_venta', 'establecimiento', 'tipo_venta', 'valor_total_display', 'ovejas_asociadas')
    list_filter = ('tipo_venta', 'fecha_venta', 'establecimiento')
    search_fields = ('id', 'ovejas__nombre', 'establecimiento__nombre')
    ordering = ('-fecha_venta',)

    def valor_total_display(self, obj):
        """
        Displays the total value of the sale formatted as currency.
        
        Args:
            obj (Venta): The sale object to format the total value for.

        Returns:
            str: The total value of the sale formatted as currency, or '-' if no value is set.
        """
        return f"${obj.valor:.2f}" if obj.valor else "-"
    valor_total_display.short_description = "Valor Total"

    def ovejas_asociadas(self, obj):
        """
        Displays a comma-separated list of sheep associated with the sale.
        
        Args:
            obj (Venta): The sale object to retrieve associated sheep for.

        Returns:
            str: A comma-separated list of sheep's RP (registration numbers) associated with the sale.
        """
        return ", ".join([str(oveja.RP) for oveja in obj.ovejas.all()])
    ovejas_asociadas.short_description = "Ovejas"

    def get_form(self, request, obj=None, **kwargs):
        """
        Customizes the form to pass the current request to the form instance.

        Args:
            request (HttpRequest): The current request being processed.
            obj (Optional[Model]): The model instance being edited, if any.
            **kwargs: Additional keyword arguments.

        Returns:
            ModelForm: The form instance with the request attached.
        """
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form


# Registrar los modelos en el admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Oveja)  # Si Oveja también necesita configuración personalizada, puedes agregar una clase Admin aquí
