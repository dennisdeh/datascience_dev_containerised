"""
Module with collection of generating objects useful for development and testing.
The focus is on simplicity (everything does what you expect it to out-of-the-box)
and versatility (many different types of data, many parameters)
"""
import pandas as pd
import random
import numpy as np
from dateutil.relativedelta import relativedelta
pd.set_option("future.no_silent_downcasting", True)


# %%
# ------------------------ #
# pandas.DataFrame's
# ------------------------ #
def gdf_single(
    n: int = 1000,
    seed: int = 42,
    max_int: int = 100,
    max_float: float = 100.0,
    max_str: int = 26,
    date_start: str = "2000-01-01",
    date_end: str = "2020-12-31",
    ratio_nans: float = 0.1,
):
    """
    Useful for generating pandas.DataFrame's with different column types.
    The ratio of missing values in the data can be controlled.

    Parameters
    ---------
    Parameters
    ---------
    n : int
        Number of rows.
    seed : int
        Random seed.
    max_int: int
        Max value of random integers generated.
    max_float: float
        Max value of random floats generated.
    max_str: int
        Max difference in the ordinal of random characters generated relative
        to ord("A")=65.
    date_start: str
        Start-date ("yyyy-mm-dd").
    date_end: str
        End-date ("yyyy-mm-dd").
    ratio_nans: float
        Missing value ratio of the generated data.

    Returns
    -------
    pd.DataFrame
        The data frame with columns:
            datetime,
            int,
            float,
            str,
            nans
    Raises
    ------
    """
    # step 0: set random seed
    random.seed(a=seed)

    """
    TODO implement a date column
    
    def f(x):
        if pd.isnull(x):
            return np.datetime64('NaT')
        else:
            return datetime(x.year, x.month, x.day)
    
    df["datetime"] = df["datetime"].apply(f)
    
    df = df.set_index("datetime")
    """

    # step 1: generate random dates
    datetimes = helper_generate_datetimes(n=n, date_start=date_start, date_end=date_end)

    # step 2: create data frame
    df = pd.DataFrame(
        {
            "datetime": datetimes,
            "int": np.random.randint(low=1, high=max_int, size=n),
            "float": np.random.uniform(low=0, high=max_float, size=n),
            "str": [
                chr(65 + x) for x in np.random.randint(low=0, high=max_str, size=n)
            ],
        }
    )

    # step 3: generate and insert random missing values
    df = df.mask(np.random.random(df.shape) < ratio_nans)
    df["int"] = df["int"].astype("Int64")

    return df


def gdf(
    n: int = 1000,
    n_copies: int = 1,
    seed: int = 42,
    max_int: int = 100,
    max_float: float = 100.0,
    max_str: int = 26,
    date_start: str = "2000-01-01",
    date_end: str = "2020-12-31",
    ratio_nans: float = 0.1,
):
    """
    This tool is useful for generating pandas.DataFrame's with many types of data.
    The ratio of missing values can be controlled. The function makes n_copies
    of each column type, each generated with a different random seed.

    Parameters
    ---------
    n : int
        Number of rows.
    n_copies : int
        Number of columns with the same data type. All additional columns get
        the suffix "_i" for 1<=i<=n_copies.
    seed : int
        Random seed.
    max_int: int
        Max value of random integers generated.
    max_float: float
        Max value of random floats generated.
    max_str: int
        Max difference in the ordinal of random characters generated relative
        to ord("A")=65.
    date_start: str
        Start-date ("yyyy-mm-dd").
    date_end: str
        End-date ("yyyy-mm-dd").
    ratio_nans: float
        Missing value ratio of the generated data.


    Returns
    -------
    pd.DataFrame
        The data frame with column types:
            datetime,
            int,
            float,
            str
    Raises
    ------
    """

    # step 1: join many
    for copy in range(n_copies):
        if copy == 0:
            df = gdf_single(
                n=n,
                seed=seed,
                max_int=max_int,
                max_float=max_float,
                max_str=max_str,
                date_start=date_start,
                date_end=date_end,
                ratio_nans=ratio_nans,
            )
        else:
            df = df.join(
                gdf_single(
                    n=n,
                    seed=seed + copy,
                    max_int=max_int,
                    max_float=max_float,
                    max_str=max_str,
                    date_start=date_start,
                    date_end=date_end,
                    ratio_nans=ratio_nans,
                ),
                on=None,
                rsuffix="_" + str(copy),
            )
    return df


# ------------------------ #
# Helper functions
# ------------------------ #
def helper_generate_datetimes(n=100, date_start="2000-01-01", date_end="2020-12-31"):
    """
    Generates a list of random datetime objects with timestamps between
    a given start and end date.

    Parameters
    ----------
    n: int
        Number of dates to be generated
    date_start: str
        Start-date ("yyyy-mm-dd")
    date_end: str
        End-date ("yyyy-mm-dd")

    Returns
    -------
    List of datetime objects.
    """

    date_start_dt = pd.to_datetime(date_start)
    date_end_dt = pd.to_datetime(date_end)

    start_u = date_start_dt.value // 10**9
    end_u = date_end_dt.value // 10**9

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit="s")


if __name__ == "__main__2":
    dftest = gdf(n_copies=2)
    dftest2 = gdf(ratio_nans=0)
    dftest3 = gdf(ratio_nans=1)
