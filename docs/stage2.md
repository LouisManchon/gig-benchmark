# Project Charter Development

## Project purpose

The purpose of this project is to develop a web application with an intuitive interface that aggregates betting odds from different bookmakers.
To achieve this goal, we have defined several SMART objectives that will guide the development process step by step.

## SMART Objectives

The objectives are detailed using the SMART methodology (Specific, Measurable, Achievable, Relevant, Time-bound) to ensure clarity and feasibility. These objectives represent the concrete features and functionalities that will progressively shape the application.

| Objectives | Specific | Measurable | Achievable | Relevant | Time-bound |
|------------|----------|------------|------------|----------|------------|
| Offer data visualization  | Create intuitive dashboard with clear informations. Define relevant indicators, such as top odds across bookmakers. | Dashboards will be developed iteratively, in collaboration with our tutor, to ensure that data organization is relevant and useful. | This feature needs to learn new langages : PHP and Symfony. By taking time we can achieve this feature.| Mandatory feature for the good comprehension of data we're scrapped. | 1 to 2 weeks to do it. |
| Collect all required betting odds | Scrape websites to provide odds with specific filters. | We are going to scrap value by value, to increase our capacities in time. We have define with our tutore what sports we have to do it in priority. | This feature needs to learn a new knowledge about scrapping websites with Python libraries. | Mandatory feature to have all data we need for the dashboard. | 1 to 2 weeks |
| Filters categories | Add some filters for sports, championship, teams or players.  | Filters will be added one by one until all categories are represented. | We have already did filters in previous projects, the numbers are just higher here. | It's a demande from our tutor to have these filters to select according to needs of the team. | 3-4 days |
| Provide admin and user accounts | Admin can choose some settings like time between every scrap, sports enable, etc. | We are going to add an user account and an admin account with one by one fonctionnality, the priority fonctionnality is to choose the delay for the scrapping and update of betting odds.| We already have implement two types of accounts in a previous project. | This feature is necessary to manage the application and accounts. | 1 week |



## Stackeholders and Team Roles

The success of the project relies on well-structured collaboration between team members. Each role has been carefully assigned to ensure that technical, organizational, and managerial aspects are covered.
With the team structure clarified, we can now delimit the scope of the project to make sure efforts remain focused and realistic.

### Team Roles

| Role | Responsabilities | Affectation | 
|------------|----------|------------|
| Project Manager | Coordinates the project, ensures deadlines are met | Dorine LEMEE |
| Database Administrator | Designs schema, manages performance and integrity | Simon PAULIN |
| DevOps | Manages deployment, Docker environments | Simon PAULIN |
| Front-end developer | Develops the user interface, ensures responsiveness | Dorine LEMEE |
| Back-end developer | Implements business logic, API, database connections | Louis MANCHON |
| Scrapper | Develops and maintains scraping scripts | Simon PAULIN |

### Stakeholders

| Stakeholder | Role/Interest | Influence on Project | 
|------------|----------|------------|
| Tutor | Provides guidance, validates technical and functional choices, ensures alignment with project objectives. | High : validates deliverables and scope. |
| End-Users | Use the platform to compare odds and evaluate usability. Provide feedback on dashboard and filters. | Medium : their feedback impacts usability and relevance. |
| Development Team | Designs, develops, deploys, and maintains the application. | Low : they maintains application after the end of the project. |
| University | Define academic expectations, deadlines, and evaluation criteria. | High : determine constraints and final assessment. |

## Scopes

The scope defines what will be included in the project (in-scope) and what will be intentionally excluded (out-of-scope). This helps avoid unnecessary complexity and ensures alignment with the tutor’s expectations.
However, even with a well-defined scope, certain risks remain and must be anticipated.

### In-Scope

| Feature | Description |
|------------|----------|
| Web platform to retrieve betting informations | Creation of a website with all information provided. |
| Create users profiles | Have the possibilities to have an user and admin account, with authentification. |
| Filters | Add filters to let users select the information they need. |
| Dashboard | Make the website the most intuitive as possible with a dashboard, like tops of bookmakers. |
| Settings | In admin settings, give possibility to choose the refresh interval for information updates |
| Calculate TRJ | Calculate TRJ from betting odds and retrieve as a top with bookmakers.|
| Alerts | We want to send an email when there is a significant variance in coasts.|
| Language | The website will be in english. |


### Out-of-Scope

| Feature | Description |
|------------|----------|
| Mobile App | We are just doing a website. |
| Scrap from bookmakers | Scrapping directly from bookmakers is really difficult, we are going to scrap from referentials betting coasts websites. |
| All sports | We concentrated on only few sports for the moment. |
| Notifications | We just want to send emails for alerts. |
| Translation | The website will be in english. |

## Risks Identified

Several risks could affect the timeline or quality of the project, such as technical learning curves, scraping challenges, or coordination issues. Identifying them early allows us to establish mitigation strategies and to adapt if necessary.
With risks accounted for, we can move on to the high-level plan that structures the development process across eight weeks.

| Risk | Probability | Impact | Strategy |
|------------|----------|----------|----------|
| Technical learning curve (Symfony, PHP, Python scraping) | High | High | Allocate learning time, use tutorials, pair programming within the team. |
| Scraping limitations (protected sites, IP blocking) | Medium | High | Use robust library, manage proxies, limit request frequency. |
| Data inconsistency (different odds from different sources) | Medium | Medium | Define a clear aggregation and display logic, validate source relevance with the tutor. |
| Team coordination (role distribution and dependencies) | Medium | Medium | Set up weekly meetings, track progress with Trello/GitHub Projects, ensure clear communication. |
| Time constraints (end of semester deadline) | High | High | Break down work into small deliverables (MVP), validate frequently with the tutor, prioritize essential features. |

## High-level Plan

Phase 1 :  Project Setup & Knowledge Acquisition (Week 1)
- Initialize Git repository, assign roles.
- Set up development environment (Symfony, Python).
- Research scraping techniques and data visualization methods.

Phase 2 : Data Scraping Module (Weeks 2–3)
- Develop a basic scraper for a reference betting site.
- Implement priority filters (sport, championship).
- Validate data relevance with the tutor.

Phase 3 : Back-end Development (Weeks 3–4)
- Set up the database.
- Build API to expose scraped data.
- Implement TRJ calculations.

Phase 4 : Front-end & Dashboard (Weeks 4–5)
- Design dashboard with clear odds visualization.
- Integrate user filters.
- Conduct usability testing with the tutor.

Phase 5 : Accounts & Admin Features (Week 6)
- Implement authentication system (user/admin).
- Develop admin settings (scraping delay, enabled sports).

Phase 6 : Testing & Risk Management (Week 7)
- Run unit and functional tests.
- Verify scraper stability.
- Adjust visualizations based on feedback.

Phase 7 : Deployment & Final Presentation (Week 8)
- Deploy on server/VM or Docker.
- Prepare final presentation and user documentation.




