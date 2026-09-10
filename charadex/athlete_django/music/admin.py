from django.contrib import admin
from .models import Character, Favorite


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "universe", "character_type", "gender", "creator", "is_featured")
    list_filter = ("universe", "character_type", "gender", "is_featured")
    search_fields = ("name", "real_name", "power", "description")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "character", "created_at")
    search_fields = ("user__username", "character__name")
