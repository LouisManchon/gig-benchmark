# User stories

### Must Have

Scraping:
- As a system, I want to scrape betting odds from Coteur.com, so that I can collect real-time sports betting data.

Queueing:
- As a system, I want to send scraped odds to RabbitMQ, so that the data pipeline is decoupled and scalable.

Consumption:
- As a consumer service, I want to read messages from RabbitMQ, so that I can insert odds into the database reliably.

Storage:
- As a data analyst, I want to store scraped odds in a structured database, so that I can query and analyze them later.

### Should Have

Data Cleaning:
- As a developer, I want to clean/normalize odds, so that the data is consistent.

Error Handling:
- As a system, I want to handle scraping or network errors gracefully, so that the pipeline does not crash.

### Could Have

Dashboard:
- As a user, I want to see scraped odds in a simple dashboard (table/chart), so that I can visualize betting trends.

Filtering:
- As a user, I want to filter matches by competition/team, so that I only see relevant odds.

### Won’t Have

User Authentication:
- Not needed for MVP.

# Mock-up

# Design System Architecture

<img/>

# Class Diagram

<img>

# Database Diagram

<img>

# High-Level Diagrams

## 1. Scraper fetches match odds and sends to message queue

## 2. WebApp displays match odds to user

## 3. User applies filters to refine displayed odds

# Externals and Internals APIs

## Externals API

|API|Purpose|
|---|--------|
|None currently|The project scrapes data directly from the target betting website, so no external odds API is required.|

## Internals API

### Endpoint: List all odds for a given match

|Field|Description|
|---|--------|
|URL Path|/api/match/|
|HTTP Method|GET|
|Input|Path parameter: match_id|
|Output|JSON array of bookmaker odds|
```
[
  {
    "bookmaker": "Pmu",
    "cote_1": "3.50",
    "cote_N": "3.60",
    "cote_2": "2.00"
  },
  {
    "bookmaker": "Vbet",
    "cote_1": "3.38",
    "cote_N": "3.64",
    "cote_2": "2.00"
  }
]
```

### Endpoint: Filter odds by bookmaker

|Field|Description|
|---|--------|
|URL Path|/api/odds?bookmaker=Pmu|
|HTTP Method|GET|
|Input|Query parameter: bookmaker|
|Output|JSON array of matches with odds only for the selected bookmaker|

```
[
  {
    "match": "STRASBOURG - MARSEILLE",
    "bookmaker": "Pmu",
    "cote_1": "3.50",
    "cote_N": "3.60",
    "cote_2": "2.00"
  }
]
```

### Endpoint: Add new scraped odds (used by producer)

|Field|Description|
|---|--------|
|URL Path|/api/odds|
|HTTP Method|POST|
|Output|JSON body|

```
[
  {
    "match": "STRASBOURG - MARSEILLE",
    "bookmaker": "Pmu",
    "cote_1": "3.50",
    "cote_N": "3.60",
    "cote_2": "2.00"
  }
]
```

