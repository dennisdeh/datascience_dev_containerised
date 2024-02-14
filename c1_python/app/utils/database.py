import os
import pandas as pd
import hashlib
from datetime import datetime
from sqlalchemy import create_engine

# global variables
data_db_name = "data"
runs_db_name = "runs"
runs_table_name = "meta"


def save(df: pd.DataFrame,
         table_name: str):
    """
    Save the data frame to the database.

    :param df: Dataframe to save
    :param table_name: name of
    """
    # 1: create a table with data and save it
    engine = create_engine(f'mysql+mysqlconnector://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@'
                           f'{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{data_db_name}')
    conn = engine.connect()
    df.to_sql(name=table_name,
              con=conn,
              if_exists="fail")
    conn.close()

    # 2: save meta_data
    engine = create_engine(f'mysql+mysqlconnector://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@'
                           f'{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{runs_db_name}')
    conn = engine.connect()
    df_meta = pd.DataFrame(data={"table_name": table_name,
                                 "hierarchy": "data",
                                 "time_stamp": str(datetime.today()),
                                 "hash": hashlib.sha1(pd.util.hash_pandas_object(df).values).hexdigest()}, index=[0])
    df_meta.to_sql(name=runs_table_name,
                   con=conn,
                   index=False,
                   if_exists="append")
    conn.close()


def load(table_name: str):
    """
    Load the data from the database

    :param table_name:
    :return: pd.Dataframe
    """
    # 1: load meta-data and perform checks
    engine = create_engine(f'mysql+mysqlconnector://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@'
                           f'{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{runs_db_name}')
    conn = engine.connect()
    df_meta = pd.read_sql_table(table_name=runs_table_name, con=conn)
    conn.close()
    # check that the table exists
    if not table_name in df_meta['table_name'].values:
        raise ValueError("Table not found in the database")
    elif len(df_meta[df_meta['table_name'] == table_name]) > 1:
        print(f"Warning, multiple tables with the name '{table_name}' found in the meta-data database")
    else:
        pass

    # 2: load data
    engine = create_engine(f'mysql+mysqlconnector://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@'
                           f'{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{data_db_name}')
    conn = engine.connect()
    df = pd.read_sql_table(table_name=table_name, con=conn, index_col="index")
    conn.close()
    # treatment of data loaded from container database
    df = df.infer_objects()
    return df
