#!/usr/bin/env python3

from dags.affiliate_etl import fetch_data, transform, load_snowflake

if __name__ == "__main__":
    print("Fetching data…")
    fetch_data()
    print("Transforming…")
    transform()
    print("Loading to Snowflake…")
    load_snowflake()
    print("Done!")
