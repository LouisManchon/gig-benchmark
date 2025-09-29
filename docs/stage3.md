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
