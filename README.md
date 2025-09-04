# Sofi Affiliate Analytics

A data engineering and analytics project designed to automate ETL (Extract, Transform, Load) workflows for affiliate marketing data at SoFi.  
The pipeline ingests raw affiliate data, processes and cleans it, loads it into a relational database, and visualizes insights with **Tableau dashboards**.

---

## 🚀 Features
- **Automated ETL Pipeline** – Ingest, transform, and load affiliate data.
- **Database Integration** – PostgreSQL support (via Docker or standalone).
- **Tableau Dashboard** – Interactive visualization of affiliate performance metrics.
- **Scalable Setup** – Run locally with Python or containerized with Docker Compose.
- **Configurable** – Use environment variables for database credentials and connections.
- **Extensible** – Easily adapt scripts for new data sources or transformations.

---

## 📂 Repository Structure
```plaintext
sofi-affiliate-analytics/
│
├── create_tables.sql         # SQL schema for database setup
├── docker-compose.yml        # Docker setup for services
├── requirements.txt          # Python dependencies
├── run_etl.py                # Main ETL pipeline script
├── run_etl_standalone.py     # Local standalone ETL version
├── tableau_dashboard/        # Tableau workbook and packaged files (.twb/.twbx)
└── README.md                 # Project documentation
```
---

## 🛠️ Requirements
- Python 3.8+
- Docker & Docker Compose
- PostgreSQL (if running outside Docker)
- Tableau Desktop or Tableau Public

---

## ⚙️ Setup & Installation
 🔹 Option 1: Run with Docker (Recommended)
 
``` bash
# Clone the repository
git clone https://github.com/Aakanksha2412/sofi-affiliate-analytics.git
cd sofi-affiliate-analytics

# Build and start services
docker-compose up --build

```

This will automatically provision a PostgreSQL instance and run the ETL pipeline.

