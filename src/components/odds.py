"""
Odds class
"""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Site:
    site_key: str
    site_nice: str
    last_update: int
    odds: Dict[str, List[float]]

    def __repr__(self) -> str:
        return f'Site(site_key={self.site_key}, site_nice={self.site_nice}, ' \
               f'last_update={self.last_update}, odds={self.odds.get("h2h", [])})'


@dataclass
class Odds:
    """
    Odds object
    """
    sport_key: str
    sport_nice: str
    teams: List[str]
    commence_time: int
    home_team: str
    sites: List[Site]
    sites_count: int

    def __repr__(self) -> str:
        return f'Odds(key={self.sport_key}, nice={self.sport_nice}, teams={self.teams}, ' \
               f'commence_time={self.commence_time}, home_team={self.home_team}, sites={self.sites}, ' \
               f'sites_count={self.sites_count})'
