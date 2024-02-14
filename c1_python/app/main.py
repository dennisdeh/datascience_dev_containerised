import pandas as pd
import numpy as np
from utils.database import save, load
from utils.generate_test_data import gdf

# Example workflow:
# 0: load data from local source (here random data is generated)
df0 = gdf(n_copies=4, n=10000)
df1 = gdf(n_copies=10, n=100)
print(df0.head())
print(df1.head())

# 1: save to container database
print("Save data to database... ", end="")
save(df0, table_name="test_table0")
save(df1, table_name="test_table1")
print("Success!")

# 2: load data from container database
print("Load data from database... ", end="")
df_loaded = load(table_name="test_table0")
print("Success!")
print(df_loaded.head())
