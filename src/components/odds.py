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

    @property
    def away_team(self):
        return self.teams[abs(self.teams.index(self.home_team) - 1)]
