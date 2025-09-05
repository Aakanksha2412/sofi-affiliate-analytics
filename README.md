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
 **🔹 Option 1: Run with Docker (Recommended)**
 
``` bash
# Clone the repository
git clone https://github.com/Aakanksha2412/sofi-affiliate-analytics.git
cd sofi-affiliate-analytics

# Build and start services
docker-compose up --build

```

This will automatically provision a PostgreSQL instance and run the ETL pipeline.

**🔹 Option 2: Local Environment Setup**

``` bash
# Clone the repository
git clone https://github.com/Aakanksha2412/sofi-affiliate-analytics.git
cd sofi-affiliate-analytics

# (Optional) Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```
**➡️ Setup Database**

``` bash
# Create tables using schema
psql -U <db_user> -d <db_name> -f create_tables.sql

```
**➡️ Run ETL**

``` bash
# Using the main ETL script
python run_etl.py

# Or run standalone script without Docker
python run_etl_standalone.py

```

## 🔧 Configuration
Set up environment variables for database connection:

``` bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=your_user
export DB_PASSWORD=your_password
export DB_NAME=sofi_affiliate

```

For Windows (PowerShell):

``` bash
setx DB_HOST "localhost"
setx DB_PORT "5432"
setx DB_USER "your_user"
setx DB_PASSWORD "your_password"
setx DB_NAME "sofi_affiliate"

```
---
## 📊 Workflow

- Extract – Ingest affiliate data from sources (CSV, APIs, or files).
- Transform – Clean, validate, and standardize data.
- Load – Insert processed data into PostgreSQL tables.
- Visualize – Connect Tableau to the database and explore insights through dashboards.

---

## 📈 Tableau Dashboard

- Located in the tableau_dashboard/ folder (.twb or .twbx files).
- Connects directly to the processed PostgreSQL database.
- Provides insights such as:
   - Affiliate channel performance
   - Cost-per-acquisition (CPA) trends
   - ROI and conversion funnel efficiency
   - Time-based traffic and conversion patterns

👉 If you’re using Tableau Public, you can publish dashboards and share interactive links.

---

## 🛣️ Roadmap / Future Enhancements

- ✅ Initial ETL pipeline
- ✅ Tableau dashboard integration
- 🔲 Automated unit tests for data validation
- 🔲 Enhanced dashboard with predictive metrics
- 🔲 CI/CD for automated deployments
- 🔲 Cloud deployment support (AWS/GCP/Azure)

---

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

---
## 👩‍💻 Author

**Aakanksha Sonawane
M.S. in Information Systems | Data Engineer & Analyst GitHub Profile**
