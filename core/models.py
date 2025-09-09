from django.db import models

class Sport(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class MarketName(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="markets")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ('sport', 'code')

    def __str__(self):
        return f"{self.sport.name} - {self.name}"


class League(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="leagues")
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('sport', 'name')

    def __str__(self):
        return self.name

class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ('league', 'name')

    def __str__(self):
        return self.name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="players")
    full_name = models.CharField(max_length=150)
    nationality = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name
