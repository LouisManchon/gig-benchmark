from rest_framework import serializers
from .models import Sport, MarketName, League, Team, Player, Odds

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'code', 'name', 'created_at', 'updated_at']

class MarketNameSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)  # ← Relation imbriquée
    class Meta:
        model = MarketName
        fields = ['id', 'sport', 'code', 'name', 'created_at', 'updated_at']

class LeagueSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)  # ← Relation imbriquée
    class Meta:
        model = League
        fields = ['id', 'sport', 'code', 'name', 'country', 'created_at', 'updated_at']  # ← Ajout de `country`

class TeamSerializer(serializers.ModelSerializer):
    league = LeagueSerializer(read_only=True)  # ← Relation imbriquée
    class Meta:
        model = Team
        fields = ['id', 'league', 'name', 'created_at', 'updated_at']

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True, allow_null=True)  # ← `allow_null` car `team` peut être null
    class Meta:
        model = Player
        fields = ['id', 'team', 'name', 'nationality', 'created_at', 'updated_at']

class OddsSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)  # ← Relation imbriquée
    away_team = TeamSerializer(read_only=True)  # ← Relation imbriquée
    championship = LeagueSerializer(read_only=True)  # ← Relation imbriquée
    type_display = serializers.SerializerMethodField()  # ← Pour afficher le libellé du type de cote

    class Meta:
        model = Odds
        fields = [
            'id', 'home_team', 'away_team', 'championship', 'date',
            'type', 'type_display', 'value', 'scraped_at'
        ]
        read_only_fields = fields  # ← Tout en lecture seule (API GET only)

    def get_type_display(self, obj):
        return obj.get_type_display()  # ← Utilise la méthode du modèle pour afficher le libellé
