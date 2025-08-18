CREATE OR REPLACE DATABASE AFFILIATE_DB;
CREATE OR REPLACE SCHEMA AFFILIATE_DB.PUBLIC;

CREATE OR REPLACE TABLE AFFILIATE_DB.PUBLIC.AFFILIATE_METRICS (
  date               DATE,
  partner            VARCHAR,
  clicks             NUMBER,
  conversions        NUMBER,
  spend              FLOAT,
  revenue            FLOAT,
  cpa                FLOAT,
  funnel_efficiency  FLOAT,
  roi                FLOAT
);
