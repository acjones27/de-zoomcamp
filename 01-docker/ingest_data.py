import pandas as pd
from sqlalchemy import create_engine
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    csv_name = params.csv_name
    csv_url = params.csv_url

    # Download and unzip csv

    os.system(f"wget {csv_url} -O {csv_name}.gz")
    os.system(f"gunzip {csv_name}.gz")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df = pd.read_csv(csv_name, nrows=100)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100_000)
    for i, chunk in enumerate(df_iter):
        print(f"Inserting chunk {i}")
        chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
        chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)
        chunk.to_sql(name=table_name, con=engine, if_exists="append")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to postgres")

    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument("--table_name", help="table_name for postgres")
    parser.add_argument("--csv_url", help="url for csv data")
    parser.add_argument("--csv_name", help="name for csv file")

    args = parser.parse_args()

    main(args)
