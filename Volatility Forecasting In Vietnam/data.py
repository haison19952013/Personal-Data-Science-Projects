"""This is for all the code used to interact with the AlphaVantage API
and the SQLite database. Remember that the API relies on a key that is
stored in your `.env` file and imported via the `config` module.
"""

import sqlite3

import pandas as pd
import requests
from config import settings


class EodhdAPI:
    def __init__(self, eodhd_api_key = settings.eodhd_api_key):
        self.eodhd_api_key = eodhd_api_key

    def get_daily(self, ticker):
    
        """Get daily time series of an equity from AlphaVantage API.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the equity.

        Returns
        -------
        pd.DataFrame
            Columns are 'open', 'high', 'low', 'close', 'adjusted_close' and 'volume'.
            All columns are numeric.
        """
    
        # Send request to API
        url = f'https://eodhd.com/api/eod/{ticker}?api_token={self.eodhd_api_key}&fmt=json'
        data = requests.get(url).json()
        
        # Check if there's been an error
        if len(data) == 0:
            raise Exception(f"Invalid API call. Check if '{ticker}' is a valid ticker symbol.")
        
        # Clean results
        data = requests.get(url).json()
        df = pd.DataFrame(data)
        df.date = pd.to_datetime(df.date)
        df.set_index("date", inplace=True)
        
        # Return results
        return df 


class SQLRepository:
    def __init__(self, connection ):
        self.connection = connection

    def insert_table(self, table_name, records, if_exists='fail'):
    
        """Insert DataFrame into SQLite database as table

        Parameters
        ----------
        table_name : str
        records : pd.DataFrame
        if_exists : str, optional
            How to behave if the table already exists.

            - 'fail': Raise a ValueError.
            - 'replace': Drop the table before inserting new values.
            - 'append': Insert new values to the existing table.

            Dafault: 'fail'

        Returns
        -------
        dict
            Dictionary has two keys:

            - 'transaction_successful', followed by bool
            - 'records_inserted', followed by int
        """
        
        n_inserted = records.to_sql(name = table_name, con = self.connection, if_exists = if_exists)
        return {
            "transaction_successful": True,
            "records_inserted": n_inserted
        }

    def read_table(self, table_name, limit=None):
    
        """Read table from database.

        Parameters
        ----------
        table_name : str
            Name of table in SQLite database.
        limit : int, None, optional
            Number of most recent records to retrieve. If `None`, all
            records are retrieved. By default, `None`.

        Returns
        -------
        pd.DataFrame
            Index is DatetimeIndex "date". Columns are 'open', 'high',
            'low', 'close', 'adjusted_close' and 'volume'. All columns are numeric.
        """
        # Create SQL query (with optional limit)
        if limit is None:
            query = f"SELECT * FROM '{table_name}'"
        else:
            query = f"SELECT * FROM '{table_name}' LIMIT {limit}"
        
        # Retrieve data, read into DataFrame
        df = pd.read_sql(query, self.connection, parse_dates=["date"], index_col="date")
        
        # Return DataFrame
        return df
