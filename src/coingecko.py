import logging
from pycoingecko import CoinGeckoAPI
from requests.exceptions import HTTPError, ConnectionError

cg = CoinGeckoAPI()

# res = get_coin(coin)
#     if res != '':
#         coin = { 'name': res['name'], 'id': res['id'], 'market_cap': res['market_cap']['usd']}
#         coins.append(coin)
#     if i % 49 == 0:
#         print('Sleeping...')
#         sleep(62)
def get_coins_market_data():
    coins = []
    try:
        for i in range(1, 30):
            print(i)
            res = cg.get_coins_markets('usd', order = 'market_cap_asc', per_page = 250, page=i)
            coins += res
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
    if coin == '':
        return 'No markets available'
    try:
        res = cg.get_coin_by_id(id=coin, community_data = 'false', tickers = 'true', developer_data = 'false', sparkline = 'false', market_data = 'false', localization = 'false')
    except (ValueError, HTTPError, ConnectionError, Exception) as err:
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
