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

<img width="1031" height="698" alt="Mockup GIG" src="https://github.com/user-attachments/assets/dea0ebb6-f0c7-4c20-bd68-f24e2bb9ae15" />


# Design System Architecture

<p align=center>
<img width="200" height="650" alt="Design System Architecture" src="https://github.com/user-attachments/assets/878899fc-e7e0-4ef2-a080-6be8acda76db" />
</p>

# Class Diagram

<p align=center>
<img width="300" height="850" alt="Class diagram" src="https://github.com/user-attachments/assets/c03d76ce-a0b9-44c8-ae1c-1a607b358486" />
</p>

# Database Diagram

<p align=center>
<img width="2206" height="1202" alt="Database Design" src="https://github.com/user-attachments/assets/6b23b31b-26d9-4a04-8051-8dc1d9fc4280" />
</p>

# High-Level Diagrams

## 1. Scraper fetches match odds and sends to message queue

<img width="3840" height="1512" alt="High-Level Sequence Diagram Scraper _ Scraper fetches match odds and sends to message queue" src="https://github.com/user-attachments/assets/37541a8a-e18c-49a9-9876-2d4117fc5e59" />

## 2. WebApp displays match odds to user

<img width="3840" height="1688" alt="High-Level Sequence Diagram Scraper _ WebApp displays match odds to user" src="https://github.com/user-attachments/assets/ce4cec93-f032-4492-9011-9ed81d9cab67" />

## 3. User applies filters to refine displayed odds

<img width="3840" height="1449" alt="High-Level Sequence Diagram Scraper _ User applies filters to refine displayed odds" src="https://github.com/user-attachments/assets/70268623-a306-4cfa-91ea-38c19bf1bc30" />

# Externals and Internals APIs

## Externals API

|API|Purpose|
|---|--------|
|None currently|The project scrapes data directly from the target betting website, so no external odds API is required.|

## Internals API


- Base URL (dev): http://localhost:8000
- Prefix: /api/
- Auth: Bearer JWT via header Authorization: Bearer <token>
- Interactive docs: /swagger/ (Swagger UI), /redoc/ (ReDoc)
- Pagination: PageNumberPagination (page, page_size), default size 50
- CORS: allows http://localhost:8001 and http://127.0.0.1:8001
### 2.1 Existing endpoints (already in code)

Standard CRUD (GET/POST/GET{id}/PUT/PATCH/DELETE), protected by JWT:

- /api/sports/, /api/sports/{id}/
- /api/market-names/, /api/market-names/{id}/ ← represents “markets”
- /api/leagues/, /api/leagues/{id}/
- /api/teams/, /api/teams/{id}/
- /api/players/, /api/players/{id}/

Authentication:

- POST /api/auth/login/ → returns access + refresh
- POST /api/auth/refresh/ → returns a new access token

Swagger/ReDoc:

- GET /swagger/, GET /redoc/


### Endpoint: Add new scraped odds (used by producer)

|Field|Description|
|---|--------|
|URL Path|/api/odds|
|HTTP Method|POST|
|Output|JSON body|

### 2.2 Odds endpoints (backend contract)

Modeling notes

- MarketName holds market metadata (e.g., code: "1X2", name: "Match Winner").
- Prefer explicit keys: prices.home, prices.draw, prices.away.
- bookmaker is a string; match_id is an internal ID.

A) List odds for a match

- Method/URL: GET /api/matches/{match_id}/odds/?market_code=1X2&bookmaker=Pmu
- Auth: Bearer
- Status: 200, 401, 404
- Response item:

```
{
  "bookmaker": "Pmu",
  "market": { "code": "1X2", "name": "Match Winner" },
  "prices": { "home": "3.50", "draw": "3.60", "away": "2.00" },
  "collected_at": "2025-09-29T12:30:00Z"
}
```

B) Filter odds across matches


- Method/URL: GET /api/odds/?bookmaker=Pmu&market_code=1X2&page=1&page_size=20
- Auth: Bearer
- Status: 200, 400 (missing bookmaker), 401
- Response:

```
{
  "count": 1,
  "results": [
    {
      "match": {
        "id": 456,
        "home_team": "STRASBOURG",
        "away_team": "MARSEILLE",
        "kickoff_at": "2025-09-29T19:00:00Z"
      },
      "bookmaker": "Pmu",
      "market": { "code": "1X2", "name": "Match Winner" },
      "prices": { "home": "3.50", "draw": "3.60", "away": "2.00" },
      "collected_at": "2025-09-29T12:30:00Z"
    }
  ]
}
```

C) Ingest scraped odds

- Method/URL: POST /api/odds/
- Auth: Bearer
- Status: 201 or 207; 400 (validation), 401, 409 (duplicate ingestion_key)
- Request:
```
[
  {
    "match_id": 456,
    "bookmaker": "Pmu",
    "market_code": "1X2",
    "prices": { "home": "3.50", "draw": "3.60", "away": "2.00" },
    "collected_at": "2025-09-29T12:30:00Z",
    "ingestion_key": "4d3a3f0e-..."
  }
]
```

- Success:

```
{ "accepted": 1, "rejected": 0, "errors": [] }
```

### 2.3 Cross-cutting conventions

- Content-Type: application/json; charset=utf-8
- Timestamps: ISO 8601 UTC (e.g., 2025-09-29T12:30:00Z)
- Errors (DRF): {"detail":"..."} or {"field":["..."]}

# SCM and QA Strategies

## SCM Strategy

### Branches
- main: Stable branch for production only.
- simon, louis, dorine: Individual feature branches for each team member to develop or fix tasks.

### Git Workflow
1. Each member commits changes to their personal branch (simon, louis, dorine).
2. Once the feature is ready, open a Pull Request to merge into main.
3. Another team member performs a code review.
4. After approval, merge into main.

## QA Strategy

### Automated Testing
- pytest for Python to verify that scraping retrieves odds correctly.
- Tests to ensure RabbitMQ messages are published and stored correctly in the database.

### Manual Testing
- Verify that the webapp displays odds correctly.
- Check that filters work as expected.

### Tools
- Python/pytest for backend tests.
- Postman/Swagger for API testing.

### Deployement Pipeline
- Deploy first to a staging environment.
- Check logs and run tests.
- Merge and deploy to production after verification.
