from django.db import models
from django.utils import timezone

class Sport(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Sports'

    def __str__(self):
        return self.name

class MarketName(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="markets")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sport', 'code')
        db_table = 'MarketNames'

    def __str__(self):
        return f"{self.sport.name} - {self.name}"


class League(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="leagues")
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sport', 'name')
        db_table = 'Leagues'
        ordering = ['name']  # Tri alphabétique par défaut

    def __str__(self):
        return self.name

class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('league', 'name')
        db_table = 'Teams'

    def __str__(self):
        return self.name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="players")
    name = models.CharField(max_length=150)
    nationality = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Players'

    def __str__(self):
        return self.name


class Odds(models.Model):
    COTE_TYPES = [
        ("1", "Victoire équipe à domicile"),
        ("N", "Match nul"),
        ("2", "Victoire équipe à l'extérieur"),
        ("O2.5", "Plus de 2.5 buts"),
        ("U2.5", "Moins de 2.5 buts"),
    ]

    # Relations avec les équipes et la ligue
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='home_odds',
        verbose_name="Équipe à domicile"
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='away_odds',
        verbose_name="Équipe à l'extérieur"
    )
    championship = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name='odds',
        verbose_name="Championnat"
    )

    # Champs spécifiques aux cotes
    date = models.DateTimeField(verbose_name="Date du match")
    type = models.CharField(max_length=10, choices=COTE_TYPES, verbose_name="Type de cote")
    value = models.DecimalField(
        max_digits=10,  # Jusqu'à 9999999999.99
        decimal_places=3,  # 3 décimales pour les cotes précises (ex: 1.856)
        verbose_name="Valeur de la cote"
    )
    scraped_at = models.DateTimeField(default=timezone.now, verbose_name="Date de scrap")

    # Métadonnées
    class Meta:
        db_table = 'Odds'
        verbose_name = "Cote"
        verbose_name_plural = "Cotes"
        ordering = ['-date']  # Tri par date (du plus récent au plus ancien)
        indexes = [
            models.Index(fields=['home_team', 'away_team', 'date']),
            models.Index(fields=['championship', 'date']),
        ]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.get_type_display()}: {self.value})"
