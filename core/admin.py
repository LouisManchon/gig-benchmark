from django.contrib import admin
from .models import Sport, League, Team, Player, MarketName

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')  # Champs à afficher dans la liste
    search_fields = ('name',)      # Champ de recherche

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'id')
    list_filter = ('sport',)       # Filtre par sport

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'id')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'id')

@admin.register(MarketName)
class MarketNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
