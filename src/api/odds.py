"""
Methods relevant to the odds API.
"""
import json
import logging
import os
import sys
from typing import Optional, Dict, Any, List, Union

import requests

from src.components.odds import Odds, Site
from src.utilities.config import load_config

LOGGER = logging.getLogger(__name__)


class OddsAPI:
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialise odds API.
        :param config_file: Path to config file.
        """
        config = load_config(config_file if config_file else os.path.join(sys.prefix, 'autobet', 'config.yml'))

        self._KEY = config.get('api', {}).get('key', '')
        self._URL = config.get('api', {}).get('url', '')
        self._REGION = config.get('api', {}).get('region', 'eu')
        self._SITES = config.get('api', {}).get('sites', [])

    def request(self, method: str, **params) -> Any:
        """
        Request a URL of the API.
        :param method: Either odds or sports.
        :return: Response dictionary.
        """
        LOGGER.info('Called %s with params: %s', os.path.join(self._URL, f'{method}'), params)

        # TODO: Remove dummy calls
        if method == 'sports':
            return json.loads(open('./data/sports.json').read())['data']

        if method == 'odds':
            return json.loads(open('./data/tennis.json').read())['data']

        if method not in ['sports', 'odds']:
            raise NotImplementedError(f'Request method {method} does not exist.')

        response = requests.get(
            os.path.join(self._URL, f'{method}'),
            params={**{'api_key': self._KEY}, **params}
        )

        if response.status_code == 200:
            return json.loads(response.text).get('data', {})

        return []

    def get_sports(self) -> List[Dict[str, Any]]:
        """
        Find the list of available sports.
        :return: List of sports
        """
        return self.request('sports')

    def get_sports_key(self, group: str) -> List[str]:
        """
        Get sports keys.
        :param group: Group to search for.
        :return: List of sports keys.
        """
        LOGGER.info('Retrieving sports keys for group %s.', group)
        sports = self.get_sports()

        return [s['key'] for s in sports if s['group'] == group]

    def get_odds(self, sport: str) -> List[Odds]:
        """
        Get list of odds for a specific sport.
        :param sport: Sports keys
        :return: List of odds. 
        """""
        sports_keys = self.get_sports_key(sport)

        odds = []

        for key in sports_keys:
            if input(f'Would you like to retrieve data for {key}? [Y/n]').lower() in ['', 'y', 'yes']:
                odds_list = self.request('odds', sport=key, region=self._REGION)

                for odds_item in odds_list:
                    odds_item['sites'] = [Site(**s)
                                          for s in odds_item['sites']
                                          if s['site_key'] in self._SITES or not self._SITES]

                    odds.append(Odds(**odds_item))

        return odds
