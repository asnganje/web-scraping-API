# Price Intelligence Scraper

**An automated web scraping and price monitoring platform built with Python, FastAPI, Scrapy, Playwright, and PostgreSQL.**

Price Intelligence Scraper collects product pricing and availability data from multiple Kenyan online retailers, centralizes the information, and provides API endpoints for price comparison and historical price tracking.

The platform combines three independent retailer-specific scrapers with a centralized scraping engine that coordinates their execution and manages the overall data collection workflow.

## Features

- **Multi-retailer scraping:** Three integrated spiders for collecting product data from different online retailers.
- **Centralized scraping engine:** Coordinates scraper execution through a unified workflow.
- **Browser automation:** Uses Playwright for browser-based interaction with dynamically rendered websites.
- **REST API:** FastAPI endpoints for managing products, retailers, listings, prices, and scraping jobs.
- **Price comparison:** Retrieves pricing information across retailers for a selected product.
- **Price history:** Records historical price observations and maintains current listing prices.
- **Database management:** PostgreSQL with SQLAlchemy ORM.
- **Database migrations:** Alembic for version-controlled schema changes.
- **Containerization:** Docker-based application packaging.
- **Cloud deployment:** Backend deployed on Railway.

## Integrated Retailer Scrapers

The scraping infrastructure currently integrates three independent Scrapy spiders:

| Spider | Retailer | Responsibility |
|---|---|---|
| `digitonia` | Digitonia Systems Ltd | Product pricing and availability |
| `fahavi` | Fahavi Computers | Product pricing and availability |
| `lappyworld` | Laptops World | Laptop product pricing and availability |

Each spider handles retailer-specific extraction logic while following a shared data persistence workflow.

## Architecture

```text
                 FastAPI REST API
                        |
              Scraping Job Management
                        |
                Scraping Engine
                        |
          +-------------+-------------+
          |             |             |
       Digitonia      Fahavi      Laptops World
        Spider        Spider         Spider
          |             |             |
          +-------------+-------------+
                        |
                 Data Processing
                        |
                PostgreSQL Database
                        |
       +----------------+----------------+
       |                |                |
    Products         Retailers       Price History
       |
  Price Comparison
```

The central engine coordinates the three spiders sequentially, while FastAPI provides the interface for initiating and monitoring scraping operations.

## Technology Stack

| Technology | Purpose |
|---|---|
| [Python](https://www.python.org/) | Core programming language |
| [FastAPI](https://fastapi.tiangolo.com/) | REST API development |
| [Scrapy](https://scrapy.org/) | Web scraping framework |
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [Scrapy-Playwright](https://github.com/scrapy-plugins/scrapy-playwright) | Scrapy and Playwright integration |
| [PostgreSQL](https://www.postgresql.org/) | Relational database |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM and database operations |
| [Pydantic](https://docs.pydantic.dev/) | Data validation and settings |
| [Alembic](https://alembic.sqlalchemy.org/) | Database migrations |
| [Docker](https://www.docker.com/) | Containerization |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [Railway](https://railway.app/) | Cloud deployment |

## How It Works

1. A scraping job is initiated through the FastAPI application.
2. The central scraping engine coordinates the three retailer spiders.
3. Each spider extracts product names, prices, availability, and listing information.
4. The backend identifies existing products and retailers to avoid unnecessary duplication.
5. Retailer listings are created or updated.
6. Price observations are stored in the price history table.
7. Scraping job execution information is made available through the API.
8. Clients can retrieve product pricing and compare retailer offers.

## Database Models

The application uses PostgreSQL with the following core data entities:

- **Products:** Central product catalogue.
- **Retailers:** Integrated retailer information.
- **Retailer Listings:** Product-to-retailer relationships, current prices, and availability.
- **Price History:** Historical price observations.
- **Scraping Jobs:** Scraping execution status and timestamps.

## Local Installation

**Requirements:** Python, PostgreSQL, and Git.

Clone the repository:

```bash
git clone https://github.com/asnganje/web-scraping-API.git
cd web-scraping-API
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables, including your PostgreSQL `DATABASE_URL`.

Apply database migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

## API Documentation

The production backend is deployed on Railway.

- **Live API:** https://web-scraping-api-production-501a.up.railway.app
- **Swagger UI:** https://web-scraping-api-production-501a.up.railway.app/docs
- **ReDoc:** https://web-scraping-api-production-501a.up.railway.app/redoc

API routes are organized under `/api/v1`.

## Engineering Highlights

- Modular Python backend architecture.
- Multiple retailer-specific Scrapy spiders.
- Centralized scraping orchestration.
- Dynamic website extraction and browser automation.
- RESTful API development.
- Relational database design and ORM integration.
- Historical price tracking.
- Automated database migrations.
- Docker-based deployment.
- Production cloud deployment.

## Future Development

- Additional retailer integrations.
- Scheduled price monitoring.
- Price trend analytics and visualizations.
- Automated price-drop notifications.
- Advanced competitor pricing intelligence.
- Enhanced scraping reliability and monitoring.

---

**Author:** Abdulrahman Nganje

**GitHub:** [asnganje](https://github.com/asnganje)

**Project:** [Price Intelligence Scraper](https://github.com/asnganje/web-scraping-API)

*Built with Python to automate competitor price monitoring and transform retail pricing data into actionable intelligence.*