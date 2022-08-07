"""Lightweight library for querying SDQL databases at https://sportsdatabase.com/."""

from enum import Enum
from typing import Union

import requests

try:
    from pandas import DataFrame

    PANDAS_INSTALLED = True
except ImportError:
    PANDAS_INSTALLED = False

BASE_URL = 'https://s3.sportsdatabase.com'


class SDQLError(Exception):
    """SDQL exception."""


class League(str, Enum):
    """League pointing to a SDQL database."""

    NBA = 'NBA'
    WNBA = 'WNBA'
    NCAABB = 'NCAABB'
    NFL = 'NFL'
    NCAAFB = 'NCAAFB'
    CFL = 'CFL'
    DANISH_SUPERLIGA = 'Danish_Superliga'
    SCOTTISH_PREMIERSHIP = 'Scottish_Premiership'
    FIFA = 'FIFA'
    NHL = 'NHL'
    MLB = 'MLB'
    ATP = 'ATP'
    WTA = 'WTA'

    def query(self, query: str, return_df: bool = False) -> Union[DataFrame, dict]:
        """Query a SDQL database.

        Args:
            query (str): The SDQL query.
            return_df (bool): Flag to return a pandas DataFrame.
                Returns a dict by default.

        Returns:
            The results of the SDQL query either as a pandas DataFrame or dict depending
            on the value of return_df.

        Raises:
            SDQLError: There was a problem parsing the provided query.
        """
        url = f'{BASE_URL}/{self.value}/query'
        response = requests.get(url=url, params={'sdql': query})

        try:
            data = response.json()
            data = dict(zip(data['headers'], data['groups'][0]['columns']))
        except Exception as exc:
            raise SDQLError(f'Error running query: {query}') from exc

        if PANDAS_INSTALLED and return_df:
            data = DataFrame(data)

        return data
