# run_etl_standalone.py

import os
import datetime
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

# ─── 1) Configuration & constants ────────────────────────────────────────────────
SNOWFLAKE_USER      = "AAKANKSHA24"
SNOWFLAKE_PASSWORD  = "Aakanksha@2498"
SNOWFLAKE_ACCOUNT   = "RVKQHQM-XHA86415"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DATABASE  = "AFFILIATE_DB"
SNOWFLAKE_SCHEMA    = "PUBLIC"

DEFAULT_CPC           = 0.50   # Experian
DEFAULT_REV_PER_CONV  = 20.0   # Credit Karma

# ─── 2) Fetch raw CSVs ───────────────────────────────────────────────────────────
def fetch_data():
    ck  = pd.read_csv("data/creditkarma.csv", parse_dates=["date"])
    exp = pd.read_csv("data/experian.csv",   parse_dates=["date"])
    ck["partner"]  = "Credit Karma"
    exp["partner"] = "Experian"
    exp["spend"]    = exp["clicks"] * DEFAULT_CPC
    ck["revenue"]   = ck["conversions"] * DEFAULT_REV_PER_CONV
    return pd.concat([ck, exp], ignore_index=True)

# ─── 3) Transform & compute KPIs ────────────────────────────────────────────────
def transform(df):
    df = df.dropna(subset=["clicks","conversions"])
    df["cpa"]            = df["spend"] / df["conversions"]
    df["funnel_efficiency"] = df["conversions"] / df["clicks"]
    df["roi"]            = (df["revenue"] - df["spend"]) / df["spend"]
    df["date"] = df["date"].dt.date
    return df

# ─── 4) Push results to Snowflake ───────────────────────────────────────────────
def load_snowflake(df):
    conn = connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
    cur = conn.cursor()
    # Re-create each run
    cur.execute("""
    CREATE OR REPLACE TABLE AFFILIATE_METRICS (
      date               DATE,
      partner            VARCHAR,
      clicks             NUMBER,
      conversions        NUMBER,
      spend              FLOAT,
      revenue            FLOAT,
      cpa                FLOAT,
      funnel_efficiency  FLOAT,
      roi                FLOAT,
      run_date           DATE
    )
    """)

    df = df.copy()
    df["run_date"] = datetime.date.today()

    insert_sql = """
      INSERT INTO AFFILIATE_METRICS
        (date, partner, clicks, conversions, spend, revenue,
         cpa, funnel_efficiency, roi, run_date)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Ensure the columns are in exactly this order:
    cols = [
      "date","partner","clicks","conversions",
      "spend","revenue","cpa","funnel_efficiency",
      "roi","run_date"
    ]

    for row in df[cols].itertuples(index=False, name=None):
        cur.execute(insert_sql, row)

    conn.commit()
    print(f"[AFFILIATE_METRICS] wrote {len(df)} rows.")
    conn.close()



# ─── STEP 5: LOAD AB_RESULTS ──────────────────────────────────────────────────────

def load_snowflake_ab_results(df_ab):
    """Write the two-row A/B summary to AB_RESULTS via parameterized INSERT."""
    conn = connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    cur = conn.cursor()

    # 1) Re-create the AB_RESULTS table
    cur.execute("""
    CREATE OR REPLACE TABLE AB_RESULTS (
      creative           VARCHAR,
      funnel_efficiency  FLOAT,
      t_stat             FLOAT,
      p_value            FLOAT,
      run_date           DATE
    )
    """)

    # 2) Define the INSERT statement
    insert_sql = """
      INSERT INTO AB_RESULTS
        (creative, funnel_efficiency, t_stat, p_value, run_date)
      VALUES (%s, %s, %s, %s, %s)
    """

    # 3) Ensure the DataFrame has exactly those columns in order
    cols = ["creative", "funnel_efficiency", "t_stat", "p_value", "run_date"]

    for row in df_ab[cols].itertuples(index=False, name=None):
        cur.execute(insert_sql, row)

    conn.commit()
    conn.close()
    print(f"[AB_RESULTS] wrote {len(df_ab)} rows.")


def run_ab_test(df):
    """Randomly assign A/B, compute avg funnel efficiency, t_stat & p_value."""
    import numpy as np
    from scipy.stats import ttest_ind
    import datetime

    df2 = df.copy()
    np.random.seed(42)
    df2["creative"] = np.random.choice(["A","B"], size=len(df2))

    # Compute per‐group conversion rate
    grp = df2.groupby("creative")
    rates = {
        g: d["conversions"].sum() / d["clicks"].sum() 
        for g,d in grp
    }

    # Run the t-test
    t_stat, p_val = ttest_ind(
        grp.get_group("A")["funnel_efficiency"],
        grp.get_group("B")["funnel_efficiency"],
        equal_var=False
    )

    print(f"AB Test → A: {rates['A']:.1%}, B: {rates['B']:.1%}, p-value={p_val:.3f}")
    # Build a 2-row summary DataFrame
    today = datetime.date.today()
    
    return pd.DataFrame([
        {"creative":"A", "funnel_efficiency":rates["A"], "t_stat":t_stat, "p_value":p_val, "run_date":today},
        {"creative":"B", "funnel_efficiency":rates["B"], "t_stat":t_stat, "p_value":p_val, "run_date":today},
    ])


# ─── MAIN ENTRYPOINT ──────────────────────────────────────────────────────────────

def main():
    # 1) Fetch & prep
    df_raw   = fetch_data()
    df_clean = transform(df_raw)

    # 2) Load core affiliate metrics
    load_snowflake(df_clean)

    # 3) Run and collect A/B test summary
    df_ab = run_ab_test(df_clean)

    # 4) Load A/B summary into warehouse
    load_snowflake_ab_results(df_ab)

    print("All done!")

if __name__ == "__main__":
    main()
