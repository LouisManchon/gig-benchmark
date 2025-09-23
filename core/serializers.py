from rest_framework import serializers
from .models import Sport, MarketName, League, Team, Player

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fieds = ('id', 'code', 'name', 'created_at', 'updated_at')

class MarketNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketName
        fields = ('id', 'code', 'name', 'created_at', 'updated_at')

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'code', 'name', 'created_at', 'updated_at')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'league', 'name', 'created_at', 'updated_at']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'team', 'name', 'nationality', 'created_at', 'updated_at']
