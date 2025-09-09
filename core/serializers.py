from rest_framework import serializers
from .models import Sport, League, Team, Player, MarketName

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'code', 'name']

class LeagueSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    class Meta:
        model = League
        fields = ['id', 'sport', 'code', 'name', 'country']

class TeamSerializer(serializers.ModelSerializer):
    league = LeagueSerializer(read_only=True)
    class Meta:
        model = Team
        fields = ['id', 'league', 'name']

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    class Meta:
        model = Player
        fields = ['id', 'team', 'full_name', 'nationality']

class MarketNameSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    class Meta:
        model = MarketName
        fields = ['id', 'sport', 'code', 'name']
