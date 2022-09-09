# !/usr/bin/env python
# coding: utf-8

import hashlib
import hmac
import json
import logging
import time
import requests

from websocket import WebSocketApp
from webhook import send_kucoin_trade_alert
#Just define the Queue in some outside file and call it from there instead of doing a circle import

class KucoinWebSocketApp(WebSocketApp, coins):

    def __init__(self, url, api_key, api_secret, **kwargs):
        super(KucoinWebSocketApp, self).__init__(url, **kwargs)
        self._api_key = api_key
        self._api_secret = api_secret

    def _send_ping(self, interval, event, payload):
        while not event.wait(interval):
            self.last_ping_tm = time.time()
            try:
                self._request(type='ping')
            except Exception as e:
                raise e

    def _request(self, type, topic=None):
        current_time = int(time.time())
        data = {
            "id": current_time,
            "type": type,
            "topic": topic
            }
        data = json.dumps(data)
        self.send(data)

    def get_sign(self, message):
        h = hmac.new(self._api_secret.encode("utf8"), message.encode("utf8"), hashlib.sha512)
        return h.hexdigest()

    def subscribe(self, topic):
        self._request("subscribe", topic=topic)

    def unsubscribe(self, topic):
        self._request("unsubscribe", topic=topic)

def on_message(ws, message):
    # type: (KucoinWebSocketApp, str) -> None
    # handle whatever message you received
    message = json.loads(message)
    try:
        pair = message['data']['symbol']
        amount = float(message['data']['size'])
        price = float(message['data']['price'])
        side = message['data']['side']
        dollar_amount = round(amount * price, 2)
        if side == 'buy':
            side = 'bought'
        else:
            side = 'sold'
        if dollar_amount > 2000:
            content = f'```Someone {side} ${dollar_amount} of {pair} at {price}.```'
            if dollar_amount > 10000:
                content += '@everyone'
            send_kucoin_trade_alert(content)
    except Exception as e:
        logging.error(e)
    logging.info("message received from server: {}".format(message))

def on_open(ws):
    # type: (KucoinWebSocketApp) -> None
    # subscribe to channels interested
    logging.info('websocket connected')
    listed_coins = get_listed_coins()
    f = open('./Data/shitcoins.json')
    coins = json.load(f)
    tickers = []
    subscribe = '/market/match:JASMY-USDT'
    for c in coins:
        ticker = c['symbol'].upper() + '-USDT'
        tickers.append(ticker)
    logging.info('Filtering coins')
    result = list(filter(lambda x: x in listed_coins, tickers))
    for c in result:
        subscribe += ','+c
    ws.subscribe(subscribe)
    #ws.subscribe('/market/match:JASMY-USDT,AGLD-USDT,SOL-USDT,SHIB-USDT')

def get_listed_coins():
    url = 'https://api.kucoin.com/api/v1/symbols'
    res = json.loads(requests.get(url).text)
    coins = []
    for c in res['data']:
        if c['quoteCurrency'] == 'USDT':
            coins.append(c['symbol'])
    return coins
