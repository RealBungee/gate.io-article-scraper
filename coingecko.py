import logging
from pycoingecko import CoinGeckoAPI
from requests.exceptions import HTTPError

cg = CoinGeckoAPI()

def get_get_coin_markets(coin):
    try:
        res = cg.get_coin_by_id(id=coin, community_data = 'false', tickers = 'true', developer_data = 'false', sparkline = 'false', market_data = 'false', localization = 'false')
    except (ValueError, HTTPError) as err:
        logging.error(f'Error Fetching Coin Information From Coingecko! \n{err}')
        return 'No markets available'
    tickers = []
    for t in res['tickers']:
        if not(t['market']['name'] in tickers):
            tickers.append(t['market']['name'])
    return tickers
