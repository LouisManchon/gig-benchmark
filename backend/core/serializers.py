from rest_framework import serializers
from .models import Odd, Match, Bookmaker, League, Sport, Team, MarketName

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'code', 'name']

class LeagueSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    
    class Meta:
        model = League
        fields = ['id', 'code', 'name', 'country', 'sport']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class MatchSerializer(serializers.ModelSerializer):
    league = LeagueSerializer(read_only=True)
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    
    class Meta:
        model = Match
        fields = ['id', 'league', 'home_team', 'away_team', 'match_date', 'status']

class BookmakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmaker
        fields = ['id', 'code', 'name', 'website']

class MarketNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketName
        fields = ['id', 'code', 'name']

class OddSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    bookmaker = BookmakerSerializer(read_only=True)
    market = MarketNameSerializer(read_only=True)
    
    class Meta:
        model = Odd
        fields = ['id', 'match', 'bookmaker', 'market', 'outcome', 'odd_value', 'trj', 'scraped_at']
