from enum import Enum, auto

import requests

try:
    from pandas import DataFrame
    PANDAS_INSTALLED = True
except ImportError:
    PANDAS_INSTALLED = False

BASE_URL = 'https://s3.sportsdatabase.com'


class SDQLError(Exception):
    pass


class Leagues(str, Enum):
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

    def query(self, query, return_df=False):
        url = f'{BASE_URL}/{self.name}/query'
        response = requests.get(url=url, params={'sdql': query})

        try:
            data = response.json()
            data = dict(zip(data['headers'], data['groups'][0]['columns']))
        except Exception:
            raise SDQLError(f'Error running query: {query}')

        if PANDAS_INSTALLED and return_df:
            data = DataFrame(data)

        return data
