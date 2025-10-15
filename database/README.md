## 📚 Relation entre les fichiers

```
📂 database/
│
├── schema/
│   └── schema.sql          # 1️⃣ Crée la STRUCTURE des tables
│                              (Sports, Leagues, Teams, Matches, Odds...)
│
└── seeds/
    ├── 01_sports.sql       # 2️⃣ Ajoute les 4 sports (FOOT, BASK, TENN, RUGB)
    ├── 02_markets.sql      # 3️⃣ Ajoute les markets (1X2, OU, BTTS...) par sport
    ├── 03_leagues.sql      # 4️⃣ Ajoute les ligues (Ligue 1, Premier League...)
    └── 04_bookmakers.sql   # 5️⃣ Ajoute les bookmakers (Betclic, Winamax, PMU...)
```

---

## 🔄 FLUX COMPLET

```
┌─────────────────────────────────────────────────────────┐
│ 1. CRÉATION DE LA BDD                                   │
│    schema.sql → Crée les tables vides                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 2. REMPLISSAGE INITIAL (SEEDS)                          │
│    01_sports.sql    → 4 sports                          │
│    02_markets.sql   → Markets (1X2, OU...)              │
│    03_leagues.sql   → Ligues (Ligue 1...)               │
│    04_bookmakers.sql → Bookmakers (Betclic...)          │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 3. SCRAPING (dynamique)                                 │
│    scraping/src/football/ligue_1.py                     │
│    → Scrappe coteur.com                                 │
│    → Envoie à RabbitMQ queue 'odds'                     │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 4. CONSUMER (backend/consumers/consumer_odds.py)        │
│    → Lit la queue 'odds'                                │
│    → Crée dynamiquement:                                │
│       - Leagues (si manquante)                          │
│       - Teams (PSG, OM...)                              │
│       - Matches (PSG vs OM)                             │
│       - Odds (cotes + TRJ)                              │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Tables STATIQUES vs DYNAMIQUES

### **STATIQUES** (Seeds - chargés 1 fois)

```
✅ Sports         → 4 lignes (FOOT, BASK, TENN, RUGB)
✅ MarketNames    → ~30 lignes (1X2, OU, BTTS...)
✅ Bookmakers     → 15 lignes (Betclic, Winamax...)
✅ Leagues        → ~25 lignes (Ligue 1, Premier League...)
```

### **DYNAMIQUES** (Créées par le scraping)

```
🔄 Teams      → Créées automatiquement (PSG, OM, LILLE...)
🔄 Matches    → Créés automatiquement (PSG vs OM)
🔄 Odds       → Créées automatiquement (cotes + TRJ)
```
