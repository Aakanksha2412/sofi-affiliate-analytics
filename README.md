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

