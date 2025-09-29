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

## Mock-up

# Design System Architecture

<img/>

# Class Diagram

<img>

# Database Diagram

<img>




