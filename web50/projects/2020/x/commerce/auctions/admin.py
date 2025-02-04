
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Auction, Bid, Comment, Watchlist

# Personalización de la visualización de User en el admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'address', 'phone')
    search_fields = ('username', 'email')

# Personalización de la visualización de Category en el admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Personalización de la visualización de Auction en el admin
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_bid', 'category', 'created_by', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description')

# Personalización de la visualización de Bid en el admin
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('auction__title', 'user__username')

# Personalización de la visualización de Comment en el admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('auction__title', 'user__username', 'content')

# Personalización de la visualización de Watchlist en el admin
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'auction__title')

# Registrar los modelos en el admin
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)