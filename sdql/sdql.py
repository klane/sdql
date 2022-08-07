"""Lightweight library for querying SDQL databases at https://sportsdatabase.com/."""

from enum import Enum, auto
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


class League(Enum):
    """League pointing to a SDQL database."""

    NBA = auto()
    WNBA = auto()
    NCAABB = auto()
    NFL = auto()
    NCAAFB = auto()
    CFL = auto()
    Danish_Superliga = auto()
    Scottish_Premiership = auto()
    FIFA = auto()
    NHL = auto()
    MLB = auto()
    ATP = auto()
    WTA = auto()

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
        url = f'{BASE_URL}/{self.name}/query'
        response = requests.get(url=url, params={'sdql': query})

        try:
            data = response.json()
            data = dict(zip(data['headers'], data['groups'][0]['columns']))
        except Exception as exc:
            raise SDQLError(f'Error running query: {query}') from exc

        if PANDAS_INSTALLED and return_df:
            data = DataFrame(data)

        return data
