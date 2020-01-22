"""
Find profitable bets automatically.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

from src.components.odds import Odds

LOGGER = logging.getLogger(__name__)


@dataclass
class AutoBetStats:
    """Allow easily accessible statistics object creation"""
    min_index: int
    min_value: float
    max_index: int
    max_value: float

    def sure_bet(self, other: AutoBetStats) -> Tuple[bool, int, int]:
        """Determine whether a sure bet can be found"""
        sure_bet_max = 1 / self.max_value + 1 / other.max_value

        if sure_bet_max < 1:
            return True, self.max_index, other.max_index

        return False, 0, 0

    def sure_bet_profit(self, other: AutoBetStats) -> float:
        """Determine the most profitable bet."""
        return 1 - (1 / self.max_value + 1 / other.max_value)


class AutoBet:
    """
    Automatically find the right bets.
    """

    def __init__(self, odds: List[Odds]):
        """Initialise instance."""
        self._odds = odds

    @staticmethod
    def minmax(odds: List[float]) -> AutoBetStats:
        """Find the minimum and maximum values for the odds across all sites."""
        min_index, min_value = min(enumerate(odds), key=lambda p: p[1])
        max_index, max_value = max(enumerate(odds), key=lambda p: p[1])

        return AutoBetStats(min_index, min_value, max_index, max_value)

    def make_suggestions(self) -> List[Dict[str, Any]]:
        """Make suggestions for sure bets."""
        suggestions = []
        for match in self._odds:
            if match.sites:
                odds_home = AutoBet.minmax([s.odds['h2h'][0] for s in match.sites])
                odds_away = AutoBet.minmax([s.odds['h2h'][1] for s in match.sites])

                sure_bet, home_index, away_index = odds_home.sure_bet(odds_away)

                if sure_bet:
                    LOGGER.info('%s vs %s is a sure bet.', match.home_team, match.away_team)

                    suggestions.append({
                        'home_team': match.home_team,
                        'away_team': match.away_team,
                        'home': match.sites[home_index].site_nice,
                        'away': match.sites[away_index].site_nice,
                        'profit': odds_home.sure_bet_profit(odds_away)
                    })

                else:
                    LOGGER.debug('%s vs %s is not a sure bet.', match.home_team, match.away_team)

        if not suggestions:
            LOGGER.info('Could not find any sure bets.')

        return suggestions
