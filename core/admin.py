from django.contrib import admin
from .models import Sport, League, Team, Player, MarketName

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')  # Champs à afficher dans la liste
    search_fields = ('name',)      # Champ de recherche
    readonly_fields = ('created_at', 'updated_at')  # ✅ Champs en lecture seule

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'id', 'created_at', 'updated_at')
    list_filter = ('sport',)       # Filtre par sport
    readonly_fields = ('created_at', 'updated_at')  # Empêche la modification manuelle

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'id', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'id', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(MarketName)
class MarketNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
