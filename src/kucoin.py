import json
import logging
import requests
import random
import time
import string
from requests.exceptions import SSLError
from http.client import RemoteDisconnected
from xmlrpc.client import ProtocolError
from time import sleep
from kucoinWebsocket import KucoinWebSocketApp, on_message, on_open
from text_processing import get_mexc_coin, concat_markets
from coingecko import get_coin_markets
from webhook import send_kucoin_listing_alert
from webSocketQueue import addTicker

def get_kucoin_announcement():
    """
    Retrieves new coin listing announcements from Kucoin
    """
    logging.debug("Pulling announcement page")
    # Generate random query/params to help prevent caching
    rand_page_size = random.randint(1, 200)
    letters = string.ascii_letters
    random_string = "".join(random.choice(letters) for i in range(random.randint(10, 20)))
    random_number = random.randint(1, 99999999999999999999)
    queries = [
        "page=1",
        f"pageSize={str(rand_page_size)}",
        "category=listing",
        "lang=en_US",
        f"rnd={str(time.time())}",
        f"{random_string}={str(random_number)}",
    ]
    random.shuffle(queries)
    logging.debug(f"Queries: {queries}")
    request_url = (
        f"https://www.kucoin.com/_api/cms/articles?"
        f"?{queries[0]}&{queries[1]}&{queries[2]}&{queries[3]}&{queries[4]}&{queries[5]}"
    )
    latest_announcement = requests.get(request_url)
    if latest_announcement.status_code == 200:
        try:
            logging.debug(f'X-Cache: {latest_announcement.headers["X-Cache"]}')
        except KeyError:
            # No X-Cache header was found - great news, we're hitting the source.
            pass

        latest_announcement = latest_announcement.json()
        logging.debug("Finished pulling announcement page")
        return latest_announcement["items"][0]
    else:
        logging.error(f"Error pulling kucoin announcement page: {latest_announcement.status_code}")
        return ""

def kucoin():
    announcements = get_kucoin_announcement()
    while(True):
        try:
            new_announcement = get_kucoin_announcement()
        except (RemoteDisconnected, ConnectionError, ProtocolError, SSLError, Exception) as e:
            logging.exception(f'Error fetching new annoucements: {e}')
        if new_announcement != announcements:
            try:
                coin =  get_mexc_coin(new_announcement['title'])
            except IndexError as err:
                print('Index error: ', err)
            exchanges = concat_markets(get_coin_markets(coin))
            url = 'https://www.kucoin.com/news'+ new_announcement['path']
            send_kucoin_listing_alert(new_announcement['title'], url, exchanges)
            logging.info('NEW LISTING ALERT')
        announcements = new_announcement
        timeout = random.randint(50, 70)
        logging.info(f'Looking for new annoucements in {timeout} seconds')
        sleep(timeout)

def get_listed_coins():
    url = 'https://api.kucoin.com/api/v1/symbols'
    res = json.loads(requests.get(url).text)
    coins = [c['baseCurrency'] for c in res['data'] if c['quoteCurrency'] == 'USDT']
    return coins

def get_listed_coin_symbols():
    url = 'https://api.kucoin.com/api/v1/symbols'
    res = json.loads(requests.get(url).text)
    coins = [c['symbol'] for c in res['data'] if c['quoteCurrency'] == 'USDT']
    return coins

def filter_listed_coins():
    listed_coins = get_listed_coin_symbols()
    f = open('./Data/shitcoins.json')
    coins = json.load(f)
    tickers = [c['symbol'].upper() + '-USDT' for c in coins]
    filtered_tickers = list(filter(lambda x: x in tickers, listed_coins))
    return filtered_tickers

def prepare_tickers():
    tickers = filter_listed_coins()
    instance_count = 0
    for index, t in enumerate(tickers):
        if index != 0 and index % 100 == 0:
            instance_count += 1
        addTicker(t)
    return instance_count

def start_kucoin_websocket():
    instance_count = prepare_tickers()
    res = requests.post('https://api.kucoin.com/api/v1/bullet-public')
    data = json.loads(res.text)
    public_token = data['data']['token']
    connect_id = 123456
    websocket_url = f'wss://ws-api.kucoin.com/endpoint?token={public_token}&[connectId={connect_id}]'
    app = KucoinWebSocketApp(websocket_url,'', '', on_open=on_open, on_message=on_message)
    app.run_forever(ping_interval=5)