"""
Django Admin Interface Configuration
"""
from django.contrib import admin
from .models import Sport, MarketName, League, Team, Match, Bookmaker, Odd


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'created_at']
    search_fields = ['code', 'name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MarketName)
class MarketNameAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'sport', 'created_at']
    list_filter = ['sport']
    search_fields = ['code', 'name']
    ordering = ['sport', 'name']
    readonly_fields = ['created_at']


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport', 'country', 'code', 'created_at']
    list_filter = ['sport', 'country']
    search_fields = ['name', 'code', 'country']
    ordering = ['sport', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'league', 'created_at']
    list_filter = ['league__sport', 'league']
    search_fields = ['name']
    ordering = ['league', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Bookmaker)
class BookmakerAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'website', 'created_at']
    search_fields = ['code', 'name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['get_match_name', 'league', 'match_date', 'status', 'created_at']
    list_filter = ['status', 'league__sport', 'league', 'match_date']
    search_fields = ['home_team__name', 'away_team__name']
    date_hierarchy = 'match_date'
    ordering = ['-match_date']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_match_name(self, obj):
        return f"{obj.home_team.name} vs {obj.away_team.name}"
    get_match_name.short_description = 'Match'


@admin.register(Odd)
class OddAdmin(admin.ModelAdmin):
    list_display = ['get_match', 'market', 'bookmaker', 'outcome', 'odd_value', 'trj', 'scraped_at']
    list_filter = ['bookmaker', 'market', 'scraped_at', 'trj']
    search_fields = ['match__home_team__name', 'match__away_team__name']
    date_hierarchy = 'scraped_at'
    ordering = ['-scraped_at']
    readonly_fields = ['created_at']
    
    def get_match(self, obj):
        return f"{obj.match.home_team.name} vs {obj.match.away_team.name}"
    get_match.short_description = 'Match'