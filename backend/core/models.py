"""
Django Models for GIG Database
Corresponds to existing MySQL tables
"""
from django.db import models
from django.utils import timezone


class Sport(models.Model):
    """Available sports (Football, Basketball, Tennis, Rugby)"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Sports'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class MarketName(models.Model):
    """Betting market types by sport"""
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='markets')
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'MarketNames'
        unique_together = [['sport', 'code']]
        ordering = ['sport', 'name']
        indexes = [
            models.Index(fields=['sport', 'code'], name='idx_sport_market'),
        ]

    def __str__(self):
        return f"{self.sport.code} - {self.name}"


class League(models.Model):
    """Leagues/Competitions"""
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='leagues')
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Leagues'
        unique_together = [['sport', 'name']]
        ordering = ['sport', 'name']
        indexes = [
            models.Index(fields=['sport'], name='idx_sport_league'),
        ]

    def __str__(self):
        return f"{self.name} ({self.sport.code})"


class Team(models.Model):
    """Teams"""
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Teams'
        unique_together = [['league', 'name']]
        ordering = ['league', 'name']
        indexes = [
            models.Index(fields=['league'], name='idx_team_league'),
        ]

    def __str__(self):
        return f"{self.name} ({self.league.name})"


class Bookmaker(models.Model):
    """Available bookmakers (TRJ is stored per match in Odds table)"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Bookmakers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Match(models.Model):
    """Upcoming or past matches"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('finished', 'Finished'),
        ('postponed', 'Postponed'),
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    match_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Matches'
        ordering = ['match_date']
        indexes = [
            models.Index(fields=['match_date'], name='idx_match_date'),
            models.Index(fields=['status'], name='idx_match_status'),
            models.Index(fields=['league'], name='idx_match_league'),
        ]

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} - {self.match_date.strftime('%Y-%m-%d')}"


class Odd(models.Model):
    """Scraped odds from bookmakers (TRJ per match)"""
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='odds')
    market = models.ForeignKey(MarketName, on_delete=models.CASCADE, related_name='odds')
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE, related_name='odds')
    outcome = models.CharField(max_length=50)  # '1', 'X', '2', 'Over', 'Under', etc.
    odd_value = models.DecimalField(max_digits=6, decimal_places=2)
    trj = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Player Return Rate (%) for this specific match/bookmaker"
    )
    scraped_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Odds'
        ordering = ['-scraped_at']
        indexes = [
            models.Index(fields=['match'], name='idx_odds_match'),
            models.Index(fields=['scraped_at'], name='idx_odds_scraped'),
            models.Index(fields=['bookmaker'], name='idx_odds_bookmaker'),
        ]

    def __str__(self):
        trj_str = f" (TRJ: {self.trj}%)" if self.trj else ""
        return f"{self.match} - {self.market.name} {self.outcome}: {self.odd_value} ({self.bookmaker.name}{trj_str})"