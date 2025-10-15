# 📊 EXPLICATIONS - Base de Données GIG

Guide complet pour comprendre la structure et le fonctionnement de la database.

---

## 🎯 Vue d'ensemble

La base de données GIG stocke les **cotes sportives** scrapées depuis coteur.com.

**Objectif :** Comparer les cotes de différents bookmakers pour trouver les meilleures opportunités.

---

## 🏗️ Architecture générale

```
┌─────────────────────────────────────────────────────┐
│                    DATABASE GIG                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────┐                                         │
│  │ Sports │ (4 sports : Foot, Basket, Tennis, Rugby)│
│  └───┬────┘                                         │
│      │                                               │
│      │ sport_id                                      │
│      ↓                                               │
│  ┌─────────┐         ┌────────────┐                │
│  │ Leagues │←────────│MarketNames │                │
│  └────┬────┘         └────────────┘                │
│       │              (1X2, OU, etc.)                │
│       │                                              │
│       │ league_id                                    │
│       ↓                                              │
│  ┌───────┐                                          │
│  │ Teams │                                          │
│  └───┬───┘                                          │
│      │                                               │
│      │ home_team_id / away_team_id                  │
│      ↓                                               │
│  ┌─────────┐                                        │
│  │ Matches │                                        │
│  └────┬────┘                                        │
│       │                                              │
│       │ match_id                                     │
│       ↓                                              │
│  ┌──────┐    ┌────────────┐                        │
│  │ Odds │───→│ Bookmakers │                        │
│  └──────┘    └────────────┘                        │
│  (+ TRJ)                                            │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 📚 Tables détaillées

### 1️⃣ Table `Sports`

**Rôle :** Liste des sports disponibles dans l'application

**Colonnes :**

- `id` : Identifiant unique (1, 2, 3, 4)
- `code` : Code court du sport (FOOT, BASK, TENN, RUGB)
- `name` : Nom complet (Football, Basketball, Tennis, Rugby)
- `created_at` / `updated_at` : Dates de création/modification

**Données :**

```
+----+------+------------+
| id | code | name       |
+----+------+------------+
| 1  | FOOT | Football   |
| 2  | BASK | Basketball |
| 3  | TENN | Tennis     |
| 4  | RUGB | Rugby      |
+----+------+------------+
```

---

### 2️⃣ Table `MarketNames`

**Rôle :** Types de paris disponibles par sport

**Colonnes :**

- `id` : Identifiant unique
- `sport_id` : Sport concerné (FK → Sports)
- `code` : Code court du marché (1X2, OU, BTTS)
- `name` : Nom descriptif ("1X2 (Match Winner)")

**Exemples de données :**

```
Football:
- 1X2 (Match Winner)
- OU (Over/Under Goals)
- BTTS (Both Teams To Score)

Basketball:
- 1X2 (Match Winner)
- OU (Over/Under Points)
- HC (Handicap)
```

---

### 3️⃣ Table `Leagues`

**Rôle :** Compétitions sportives (Ligue 1, Premier League, NBA...)

**Colonnes :**

- `id` : Identifiant unique
- `sport_id` : Sport concerné (FK → Sports)
- `code` : Code court (LIGUE_1, PREMIER_LEAGUE)
- `name` : Nom complet ("Ligue 1")
- `country` : Pays de la ligue ("France")

**Relation avec Sports :**

```
Football (sport_id=1)
  ├─ Ligue 1 (league_id=1)
  ├─ Premier League (league_id=2)
  └─ La Liga (league_id=3)

Basketball (sport_id=2)
  ├─ NBA (league_id=4)
  └─ EuroLeague (league_id=5)
```

---

### 4️⃣ Table `Teams`

**Rôle :** Équipes participant aux compétitions

**Colonnes :**

- `id` : Identifiant unique
- `league_id` : Ligue de l'équipe (FK → Leagues)
- `name` : Nom de l'équipe ("PSG", "OM")

**Relation avec Leagues :**

```
Ligue 1 (league_id=1)
  ├─ PSG (team_id=1)
  ├─ OM (team_id=2)
  └─ Lyon (team_id=3)

Premier League (league_id=2)
  ├─ Manchester United (team_id=4)
  └─ Arsenal (team_id=5)
```

**Point important :**

- Une équipe est dans UNE SEULE ligue
- Si PSG joue en Champions League, il faut créer une entrée séparée (ou gérer les compétitions multiples)

---

### 5️⃣ Table `Bookmakers`

**Rôle :** Liste des bookmakers (Betclic, Winamax, PMU...)

**Colonnes :**

- `id` : Identifiant unique
- `code` : Code court (BETCLIC, WINAMAX)
- `name` : Nom complet ("Betclic")
- `website` : URL du bookmaker

**Données (15 bookmakers de coteur.com) :**

```
PMU, ParionsSport, ZEbet, Winamax, Betclic,
Betsson, Bwin, Unibet, OlyBet, FeelingBet,
Genybet, Vbet, Bet365, NetBet, Pinnacle
```

**⚠️ IMPORTANT : Pas de TRJ ici !**
Le TRJ (Taux de Retour Joueur) **varie par match**, donc il est stocké dans la table `Odds`.

---

### 6️⃣ Table `Matches`

**Rôle :** Matchs sportifs (à venir, en cours, ou passés)

**Colonnes :**

- `id` : Identifiant unique
- `league_id` : Ligue du match (FK → Leagues)
- `home_team_id` : Équipe à domicile (FK → Teams)
- `away_team_id` : Équipe extérieure (FK → Teams)
- `match_date` : Date et heure du match
- `status` : Statut (scheduled, live, finished, postponed)

**Exemple :**

```
Match #1:
  league: Ligue 1
  home_team: PSG
  away_team: OM
  match_date: 2025-10-15 21:00
  status: scheduled
```

**Contraintes :**

- `home_team_id` ≠ `away_team_id` (une équipe ne peut pas jouer contre elle-même)
- Les deux équipes doivent être dans la même ligue

---

### 7️⃣ Table `Odds` ⭐ **LA PLUS IMPORTANTE**

**Rôle :** Cotes scrapées depuis coteur.com avec le TRJ

**Colonnes :**

- `id` : Identifiant unique
- `match_id` : Match concerné (FK → Matches)
- `market_id` : Type de marché (FK → MarketNames)
- `bookmaker_id` : Bookmaker (FK → Bookmakers)
- `outcome` : Résultat ('1', 'X', '2')
- `odd_value` : Valeur de la cote (1.85, 3.40, 4.20)
- `trj` : **Taux de Retour Joueur (%) pour ce match/bookmaker**
- `scraped_at` : Date et heure du scraping

**Exemple concret :**

```
Match: PSG vs OM (2025-10-15 21:00)
Bookmaker: Betclic
TRJ: 91.5%

3 lignes dans Odds:
+----+----------+-----------+-------------+---------+-----------+------+
| id | match_id | market_id | bookmaker_id| outcome | odd_value | trj  |
+----+----------+-----------+-------------+---------+-----------+------+
| 1  |    1     |     1     |      5      |   1     |   1.85    | 91.5 |
| 2  |    1     |     1     |      5      |   X     |   3.40    | 91.5 |
| 3  |    1     |     1     |      5      |   2     |   4.20    | 91.5 |
+----+----------+-----------+-------------+---------+-----------+------+
```

**🔑 Point clé : Pourquoi le TRJ est ici et pas dans `Bookmakers` ?**

Le TRJ **varie par match** ! Exemple :

```
PSG vs OM : Betclic TRJ = 91.5%
Lyon vs Monaco : Betclic TRJ = 90.8%
Nice vs Lens : Betclic TRJ = 92.1%
```

Donc chaque cote a son propre TRJ.

**Pourquoi cette table ?**

- Historique complet des cotes
- Permet de comparer les bookmakers
- Trouve la meilleure cote pour un match donné

---

## 🔗 Relations entre tables

### Hiérarchie complète

```
Sport
  ↓ 1 sport → N leagues
League
  ↓ 1 league → N teams
Team
  ↓ 2 teams → 1 match
Match
  ↓ 1 match → N odds (une par bookmaker/outcome)
Odd
  → Bookmaker (qui a fourni cette cote)
  → MarketName (type de pari)
```

### Exemple de requête SQL

**Trouver toutes les cotes pour PSG vs OM :**

```sql
SELECT
    m.id as match_id,
    CONCAT(ht.name, ' vs ', at.name) as match_name,
    b.name as bookmaker,
    mk.name as market,
    o.outcome,
    o.odd_value,
    o.trj
FROM Matches m
JOIN Teams ht ON m.home_team_id = ht.id
JOIN Teams at ON m.away_team_id = at.id
JOIN Odds o ON m.id = o.match_id
JOIN Bookmakers b ON o.bookmaker_id = b.id
JOIN MarketNames mk ON o.market_id = mk.id
WHERE ht.name = 'PSG'
  AND at.name = 'OM'
  AND o.scraped_at > DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY o.outcome, o.odd_value DESC;
```

**Résultat :**

```
PSG vs OM
  Outcome '1':
    - Winamax: 1.88 (TRJ: 92.0%)  ← Meilleure cote
    - Betclic: 1.85 (TRJ: 91.5%)
    - PMU: 1.82 (TRJ: 91.0%)

  Outcome 'X':
    - Betclic: 3.40 (TRJ: 91.5%)
    - Winamax: 3.35 (TRJ: 92.0%)

  Outcome '2':
    - Betclic: 4.20 (TRJ: 91.5%)
    - Winamax: 4.10 (TRJ: 92.0%)
```

---

## 📈 Flux de données

### Comment les données arrivent en DB

```
1. Scraper coteur.com
   ↓ (Selenium)
   Extract: match, bookmaker, cotes, TRJ

2. Publish to RabbitMQ
   ↓ (queue: "odds")
   Message JSON

3. Consumer
   ↓ (consumer_odds.py)
   Parse message

4. Database
   ↓ (Django ORM)
   Create Match, Teams, Odds

5. Admin Django
   ↓ (visualisation)
   Voir les cotes avec TRJ
```

---

## 🎯 Cas d'usage

### 1. Trouver la meilleure cote pour PSG gagnant

```sql
SELECT
    b.name,
    o.odd_value,
    o.trj
FROM Odds o
JOIN Bookmakers b ON o.bookmaker_id = b.id
JOIN Matches m ON o.match_id = m.id
JOIN Teams ht ON m.home_team_id = ht.id
WHERE ht.name = 'PSG'
  AND o.outcome = '1'
  AND m.status = 'scheduled'
ORDER BY o.odd_value DESC
LIMIT 1;
```

### 2. Comparer les TRJ moyens par bookmaker

```sql
SELECT
    b.name,
    ROUND(AVG(o.trj), 2) as avg_trj,
    COUNT(o.id) as nb_cotes
FROM Odds o
JOIN Bookmakers b ON o.bookmaker_id = b.id
WHERE o.scraped_at > DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY b.id
ORDER BY avg_trj DESC;
```

### 3. Historique des cotes pour un match

```sql
SELECT
    o.scraped_at,
    b.name,
    o.outcome,
    o.odd_value
FROM Odds o
JOIN Bookmakers b ON o.bookmaker_id = b.id
WHERE o.match_id = 1
ORDER BY o.scraped_at DESC;
```

---

## ⚠️ Points d'attention

### 1. Duplication des équipes

**Problème :** Si PSG joue en Ligue 1 ET en Champions League, on doit créer 2 entrées ?

**Solution actuelle :** Oui, une équipe par ligue.

**Alternative :** Ajouter une table `Participations` (team_id, league_id, season)

### 2. Dates des matchs

**Problème :** Ton scraper ne récupère pas encore la vraie date.

**Solution temporaire :** Le consumer met "demain 20h00" par défaut.

**À faire :** Extraire la vraie date depuis coteur.com dans le scraper.

### 3. Nettoyage des vieilles cotes

**Problème :** La table `Odds` va grossir très vite (des millions de lignes).

**Solution :** Créer une tâche Celery qui supprime les cotes de plus de 30 jours :

```sql
DELETE FROM Odds
WHERE scraped_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

## 🚀 Évolutions possibles

### Court terme

- [ ] Extraire la vraie date des matchs
- [ ] Scraper d'autres ligues automatiquement

### Moyen terme

- [ ] Table `History` pour tracker l'évolution des cotes dans le temps
- [ ] Calcul automatique de la "value bet" (meilleure opportunité)
- [ ] Alertes quand une cote devient intéressante

### Long terme

- [ ] Machine Learning pour prédire les meilleures cotes

---

## 📚 Ressources

- [Documentation MySQL](https://dev.mysql.com/doc/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Coteur.com](https://www.coteur.com)

---

**Version :** 2.0  
**Dernière mise à jour :** Octobre 2025  
**Auteur :** GIG Team
