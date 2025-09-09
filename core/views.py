from rest_framework import generics
from .models import Sport, League, Team, Player, MarketName
from .serializers import SportSerializer, LeagueSerializer, TeamSerializer, PlayerSerializer, MarketNameSerializer
from django.http import JsonResponse

# List all Sports
class SportList(generics.ListCreateAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

# Retrieve a single Sport
class SportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

# Même logique pour League, Team, Player, MarketName
class LeagueList(generics.ListCreateAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

class LeagueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class MarketNameList(generics.ListCreateAPIView):
    queryset = MarketName.objects.all()
    serializer_class = MarketNameSerializer

class MarketNameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarketName.objects.all()
    serializer_class = MarketNameSerializer

def test_api(request):
    data = {
        "sports": [
            {"id": 1, "name": "Football"},
            {"id": 2, "name": "Basketball"},
        ]
    }
    return JsonResponse(data)
