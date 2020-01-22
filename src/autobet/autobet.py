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
    min_index: int
    min_value: float
    max_index: int
    max_value: float

    def __gt__(self, other: AutoBetStats) -> bool:
        return self.min_value > other.min_value

    def __lt__(self, other: AutoBetStats) -> bool:
        return not self.min_value > other.min_value

    def sure_bet(self, other: AutoBetStats) -> Tuple[bool, int, int]:
        sure_bet_max = 1 / self.max_value + 1 / other.max_value

        if sure_bet_max < 1:
            return True, self.max_index, other.max_index

        return False, 0, 0

    def sure_bet_profit(self, other: AutoBetStats) -> float:
        return 1 - (1 / self.max_value + 1 / other.max_value)


class AutoBet:
    def __init__(self, odds: List[Odds]):
        self._odds = odds

    @staticmethod
    def minmax(odds: List[float]) -> AutoBetStats:
        min_index, min_value = min(enumerate(odds), key=lambda p: p[1])
        max_index, max_value = max(enumerate(odds), key=lambda p: p[1])

        return AutoBetStats(min_index, min_value, max_index, max_value)

    def make_suggestions(self) -> List[Dict[str, Any]]:
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
