import logging
import json
from time import sleep
from pycoingecko import CoinGeckoAPI
from requests.exceptions import HTTPError, ConnectionError

cg = CoinGeckoAPI()

def get_coins_market_data():
    coins = []
    try:
        for i in range(1, 52):
            if i == 20 or i == 40:
                sleep(120)
            print('Fetching page: ', i)
            res = cg.get_coins_markets('usd', order = 'market_cap_asc', per_page = 250, page=i)
            coins += res
        print("Success!")
        return coins
    except (ValueError, HTTPError, ConnectionError, Exception) as err:
        logging.error(f'Error Fetching Coin Information From Coingecko! \n{err}')
    return []

def get_listed_coins():
    try:
        res = cg.get_coins_list(include_platform=False)
        return res
    except (ValueError, HTTPError, ConnectionError, Exception) as err:
        logging.error(f'Error Fetching Coin Information From Coingecko! \n{err}')
    return []

def get_coin(coin):
    try:
        res = cg.get_coin_by_id(id=coin, community_data = 'false', tickers = 'true', developer_data = 'false', sparkline = 'false', localization = 'false')
        return res
    except (ValueError, HTTPError, ConnectionError, Exception) as err:
        logging.error(f'Error Fetching Coin Information From Coingecko! \n{err}')
    return ''

def get_coin_markets(coin):
    if coin == '': return 'No markets available'
    try:
        res = cg.get_coin_by_id(id=coin, community_data = 'false', tickers = 'true', developer_data = 'false', sparkline = 'false', market_data = 'false', localization = 'false')
    except (ValueError, HTTPError, ConnectionError, Exception) as err:
        logging.error(f'Error Fetching Coin Information From Coingecko! \n{err}')
        return 'No markets available'
    #returns a set of exchanges where the coin is listed
    return {t['market']['name'] for t in res['tickers']}

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
        tickers.append({'trade_url':t['trade_url'], 'symbol':t['symbol']})
    exchangeTokens.append({'name':res['name'], 'exchange':exchange, 'tickers':tickers})

    return exchangeTokens
