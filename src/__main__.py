"""
Automatic bet suggestions
"""
import argparse
import logging.config
import os
import sys

from src.api.odds import OddsAPI
from src.autobet.autobet import AutoBet

logging.config.fileConfig(os.path.join(sys.prefix, 'autobet', 'logger.ini'), disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)


def main() -> None:
    """
    Parse arguments and perform main functionality.
    :return: None
    """
    parser = argparse.ArgumentParser(description='Automatically make suggestions for bets that cannot be lost.')

    parser.add_argument(
        '-c', '--config',
        default='./config.yml',
        type=str,
        help='Path to config file.',
    )

    parser.add_argument(
        '-ls', '--list-sports',
        action='store_true',
        help='Show an overview of the available sports.',
    )

    parser.add_argument(
        '-o', '--list-odds',
        action='store_true',
        help='Show odds for a specific sport.',
    )

    parser.add_argument(
        '-s', '--sport',
        default='Tennis',
        type=str,
        help='Select sport to optimise bets.',
    )

    parser.add_argument(
        '-m', '--spend', '--money',
        default=10,
        type=float,
        help='Money to spend per suggested bet.',
    )

    args, _ = parser.parse_known_args()

    api = OddsAPI()

    odds_list = []

    if args.list_sports:
        sports_list = api.get_sports()
        LOGGER.info('Listing available sports:\n%s', sports_list)

    elif args.list_odds:
        odds_list = api.get_odds(sport=args.sport)
        LOGGER.info('Listing available odds:\n%s', odds_list)

    if args.sport or \
            (args.list_odds and input('Would you like to continue to AutoBet?').lower() in ['', 'y', 'yes']):
        LOGGER.info('Finding relevant odds for sport: %s', args.sport)

        odds = odds_list if odds_list else api.get_odds(sport=args.sport)

        autobet = AutoBet(odds)
        suggestions = autobet.make_suggestions(args.spend)

        LOGGER.info('Suggestions are as follows:\n%s', suggestions)
        # ...


if __name__ == '__main__':
    main()
