# Bet automator
Find bets across multiple betting sites to find sure bets with the use of [The Odds API](https://www.the-odds-api.com/).

## Installation
```bash
# Clone the repo
$ git clone git@github.com:bartcode/bet-automator.git
# Rename config.default.yml to config.yml
$ mv config.default.yml config.yml
# Update config.yml with the right API key from the-odds-api.com.
# Install the package.
$ pip install .
```

## Usage
```text
usage: autobet [-h] [-c CONFIG] [-ls] [-o] [-s SPORT]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to config file.
  -ls, --list-sports    Show an overview of the available sports.
  -o, --list-odds       Show odds for a specific sport.
  -s SPORT, --sport SPORT
                        Select sport to optimise bets.

```
