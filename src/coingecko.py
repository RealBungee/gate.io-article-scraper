import logging
from pycoingecko import CoinGeckoAPI
from requests.exceptions import HTTPError

cg = CoinGeckoAPI()

def get_coin_markets(coin):
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

# Gets the ticker and url to all futures tokens on the inputted exchange
# e.g get_all_futures_coins("binance_futures")
def get_all_futures_coins(exchange):
    try:
        res = cg.get_derivatives_exchanges_by_id(id=exchange, include_tickers=['unexpired'])
    except (ValueError, HTTPError) as err:
        logging.error(f'Error Fetching Coin Futures Information From Coingecko! \n{err}')
        return 'No markets available'
    exchangeTokens = []
    tickers = []
    for t in res['tickers']:
        tickers.append([t['trade_url'], t['symbol']])
    exchangeTokens.append([res['name'], exchange, tickers])

    return exchangeTokens