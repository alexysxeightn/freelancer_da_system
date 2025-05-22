import pandas as pd
import sqlite3


def load_dataset_into_sqlite(path):
    df = pd.read_csv(path)
    conn = sqlite3.connect(":memory:")
    df.to_sql("freelancers", conn, index=False)
    return conn, df
