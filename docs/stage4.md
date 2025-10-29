# Sprint Planning & Development Documentation
**Project:** GIG Benchmark - Sports Betting Odds Comparison Platform  
**Team:** Dorine Lemée, Simon Paulin, Louis Manchon  
**Period:** 29/09/25 - 24/10/25

## 0. Sprint Planning

### Project Objectives
Develop a web platform to:
- Automatically scrape odds from Coteur.com
- Compare player return rates (RTP)
- Visualize odds evolution in real-time
- Filter by sport, league, bookmaker, matches and date

### Defined Sprints

#### **Sprint 1: Infrastructure & Backend** (Weeks 1)
**Must Have**
- [x] Docker configuration (Symfony, Django, RabbitMQ, MySQL)
- [x] Microservices architecture
- [x] MySQL database with models (Sport, League, Team, Match, Bookmaker, Odd)
- [x] Django REST API for data retrieval

**Should Have**
- [x] Scraping system with Selenium + RabbitMQ
- [x] Python worker for asynchronous processing
- [x] Automatic RTP calculation

**Could Have**
- [ ] Graphics with RTP evolution
- [ ] Others types of odds than Home, Draw, Away

#### **Sprint 2: Multi-Sport Scraping** (Weeks 2-3)
**Must Have**
- [x] Football Scraper: Ligue 1
- [x] Football Scraper: Premier League
- [x] Football Scraper: La Liga
- [x] Football Scraper: Serie A
- [x] Football Scraper: Bundesliga
- [x] Football Scraper: Champions League
- [x] Real-time progress system

**Should Have**
- [x] Scraping error handling
- [x] "All Leagues" option for multiple scraping
- [ ] Basketball Scrapers (NBA, Euroleague)
- [ ] Rugby Scrapers (Top 14)
- [ ] Tennis Scrapers (ATP, WTA)

**Could Have**
- [ ] Parallel scraping
- [ ] Automatic rate limiting

#### **Sprint 3: Frontend & UX** (Weeks 4)
**Must Have**
- [x] Responsive Symfony Twig interface
- [x] Filter form (Sport, Bookmaker, League, Match, Date)
- [x] Average RTP table by bookmaker
- [x] Detailed odds table per match
- [x] Scraping sidebar with progress bar
- [x] Multiple filters system

**Should Have**
- [x] Evolution indicators (↑↓→) with colors
- [x] Hover effects on tables
- [x] Date picker
- [x] CSV export
- [ ] Trend charts

**Could Have**
- [ ] Dark mode
- [ ] Real-time notifications
- [ ] Favorites system

---

### Task Distribution

| Member | Role | Main Responsibilities |
|--------|------|----------------------|
| Dorine Lemée | Frontend Developer / Backend Developer / Documentation | Symfony Interface, CSS, JavaScript, API Routes, Scrappers |
| Simon Paulin | Backend Developer / DevOps | Docker, Scrapers, RabbitMQ Worker, API Routes |
| Louis Manchon | Backend Developer | Django Interface and API Routes |

---

## 1. Development Execution

### Technical Architecture

```
┌─────────────────┐
│  Symfony (PHP)  │ ← Frontend + Routing
│   Twig / CSS    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Django (API)   │ ← REST Backend
│   MySQL         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    RabbitMQ     │ ← Message Queue
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Python Worker   │ ← Scraping
│ Selenium Remote │
└─────────────────┘
```

### Project Structure

```
gig-benchmark/
├── backend/                  # Django API
│   ├── core/
│   │   ├── models.py        # Database models
│   │   ├── views/
│   │   │   ├── data_views.py
│   │   │   └── scraping_views.py
│   │   └── urls.py
│   └── manage.py
│
├── scraping/                 # Scraping service
│   ├── src/
│   │   ├── football/
│   │   │   ├── ligue_1.py
│   │   │   ├── premier_league.py
│   │   │   ├── la_liga.py
│   │   │   ├── serie_a.py
│   │   │   ├── bundesliga.py
│   │   │   └── champions_league.py
│   │   ├── basketball/
│   │   ├── rugby/
│   │   └── tennis/
│   └── worker.py            # RabbitMQ Worker
│
├── frontend/                 # Symfony
│   ├── src/
│   │   ├── Controller/
│   │   ├── Form/
│   │   └── Entity/
│   ├── templates/
│   │   ├── base.html.twig
│   │   └── odds/index.html.twig
│   └── public/
│       ├── css/
│       │   ├── base.css
│       │   ├── sidebar.css
│       │   ├── filters.css
│       │   └── tables.css
│       └── js/
│           ├── sidebar.js
│           └── scraping.js
│
└── docker-compose.yml
```

### Git Branching Strategy

```
main
  ├── dorine
  ├── simon
  ├── louis
  
```

**Rules:**
- `main`: Stable production
- `dorine`: Branch for Dorine, especially frontend.
- `simon`: Branch for Simon, especially Docker.
- `louis`: Branch for Louis, especially backend.

### Code Standards

**Python:**
```python
# PEP 8 compliance
# Mandatory docstrings
# Type hints recommended

def scrape_ligue_1() -> dict:
    """
    Scrape all Ligue 1 matches from coteur.com
    
    Returns:
        dict: Scraping results with status, matches_scraped, odds_sent
    """
    pass
```

**PHP/Symfony:**
```php

/**
 * Get odds with filters
 * 
 * @param Request $request
 * @return JsonResponse
 */
public function getOdds(Request $request): JsonResponse
{
    // ...
}
```

**CSS:**
```css
/* Organization by thematic file */
/* Section comments */
/* Explicit class names */

/* ========================================
   TABLES - Data tables
   ======================================== */
.all_matchs {
    /* ... */
}
```

---

## 2. Progress Monitoring

### Sprint Metrics

#### Sprint 1 (Infrastructure)
- **Completed tasks:** 12/12 (100%)
- **Bugs identified:** 3
- **Bugs resolved:** 3

#### Sprint 2 (Scraping)
- **Completed tasks:** 8/10 (80%)
- **Bugs identified:** 5
- **Bugs resolved:** 4
- **Blockers:** Champions League import (resolved)

#### Sprint 3 (Frontend)
- **Completed tasks:** 15/18
- **Bugs identified:** 8
- **Bugs resolved:** 7
- **In progress:** Choices.js alignment (resolved)

### Daily Stand-ups

**Questions:**
1. What did I do yesterday?
2. What will I do today?
3. Do I have any blockers?

### Weekly Stand-up

Every tuesday, We had a call with our tutor, Morgan. With the same questiosn as daily stand-ups, and to fix objectives for next week.

### Bug Tracking

| Priority | Description | Sprint | Status |
|----------|-------------|--------|--------|
| High | Choices.js doesn't load leagues | 2 | Resolved |
| Medium | Progress bar stuck at 15/18 | 2 | In progress |
| Low | CSV export missing header | 3 | Resolved |
|  High | Champions League import error | 2 | Resolved |
| Medium | Match select auto-enlarges | 3 | Resolved |

---

## 3. Sprint Reviews & Retrospectives

### Sprint 1 Review

**Date:** [04/10/25]  

**Demos performed:**
- Functional Docker architecture (4 services)
- MySQL database with migrations
- Django API with base endpoints
- RabbitMQ configured and operational

---

### Sprint 1 Retrospective

**What went well:**
- Good team communication
- Docker Compose facilitates local development
- Effective pair programming on architecture

**What didn't go well:**
- Task estimation time underestimated
- Some Git conflicts due to long-lived branches
---

### Sprint 2 Review (Scraping)

**Date:** [14/10/25]

**Demos performed:**
- 6 operational football scrapers
- Real-time progress bar
- RabbitMQ queue system functional
- Automatic RTP calculation

**Feedback:**
- Progress interface highly appreciated
- Request: Add "All Leagues" option

---

### Sprint 2 Retrospective

**What went well:**
- Robust scraping architecture
- Effective error handling
- Regular manual testing

**What didn't go well:**
- Champions League import blocked (incorrect path)
- Progress stuck between scrapers
- Lack of automated tests

---

### Sprint 3 Review (Frontend)

**Date:** [24/10/25]

**Demos performed:**
- Complete and responsive interface
- Functional multiple filters
- Tables with colored evolutions
- Integrated scraping sidebar
- CSV export

**Feedback:**
- Clean and professional design
- Very clear progress bar
---

### Sprint 3 Retrospective

**What went well:**
- Well-organized CSS in 4 files
- Modular and reusable JavaScript
- Good responsiveness to user feedback

**What didn't go well:**
- Some features can't be add by lack of time : graphics, authetification with Keycloak.
- Website is very long to charge.
- Bad communication.


---

## 4. Final Integration & QA

### 🧪 Test Plan

#### Unit Tests (Backend)
```python
# backend/core/tests/test_scraping.py
def test_send_scraping_task():
    """Test that tasks are properly sent to RabbitMQ"""
    result = send_scraping_task('football.ligue_1')
    assert result == True

def test_calculate_trj():
    """Test RTP calculation"""
    trj = calculate_trj(2.5, 3.2, 2.8)
    assert 89.0 <= trj <= 91.0
```

#### Integration Tests (API)
```bash
# Test endpoints
curl -X POST http://localhost:8000/api/scraping/trigger \
  -H "Content-Type: application/json" \
  -d '{"scraper": "football.ligue_1"}'

# Expected response
{"success": true}
```

#### E2E Tests (Frontend)
```javascript
// tests/e2e/scraping.spec.js
test('Complete scraping workflow', async ({ page }) => {
  await page.goto('http://localhost:8080/odds');
  
  // Open sidebar
  await page.click('#toggleSidebar');
  
  // Select sport and league
  await page.selectOption('#sport-scraping', 'football');
  await page.selectOption('#league-scraping', 'ligue_1');
  
  // Start scraping
  await page.click('#start-scraping-btn');
  
  // Verify progress bar appears
  await expect(page.locator('#scraping-progress')).toBeVisible();
});
```

### Critical Bugs Identified

| ID | Description | Impact | Fix |
|----|-------------|--------|-----|
| #010 | Progress stuck at 15/18 Bundesliga | 🔴 Blocking | Missing 'completed' status |
| #011 | Champions League doesn't start | 🔴 Blocking | Check progress sending |
| #012 | Selenium timeout after 5 min | 🟡 Medium | Increase timeout to 10 min |

### Security Tests

- SQL Injections: Protected by Django ORM
- CSRF: Tokens enabled on forms
- RabbitMQ Authentication: Secured credentials
- HTTPS: To be enabled in production

---

## 5. Deliverables

### Deliverable Links

#### Sprint Reviews
- [Sprint 1 Review](./docs/sprints/sprint-1-review.md)
- [Sprint 2 Review](./docs/sprints/sprint-2-review.md)
- [Sprint 3 Review](./docs/sprints/sprint-3-review.md)
- [Sprint 4 Review](./docs/sprints/sprint-4-review.md)

#### Retrospectives
- [Sprint 1 Retrospective](./docs/sprints/sprint-1-retro.md)
- [Sprint 2 Retrospective](./docs/sprints/sprint-2-retro.md)
- [Sprint 3 Retrospective](./docs/sprints/sprint-3-retro.md)
- [Sprint 4 Retrospective](./docs/sprints/sprint-4-retro.md)

---

---

### Goals Achieved

- Functional MVP deployed
- 6 operational football scrapers
- Responsive and intuitive interface
- Real-time progress system
- CSV export
- Scalable architecture

### Future Improvements (Backlog)

1. **Phase 2 - Complete Multi-sports**
   - Basketball, Rugby, Tennis scrapers
   - Inter-sport comparison

2. **Phase 3 - Advanced Analytics**
   - Trend charts
   - Odds variation alerts
   - Long-term history

3. **Phase 4 - Premium Features**
   - Authentication system
   - Personalized favorites
   - Public API
