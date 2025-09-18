from rest_framework import serializers
from .models import Sport, MarketName, League, Team, Player

class SportSerializer(serializers.ModelField):
    class Meta:
        model = Sport
        fieds = ('id', 'code', 'name')

class MarketNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketName
        fields = ('id', 'code', 'name')

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'code', 'name')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'league', 'name']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'team', 'full_name', 'nationality']
