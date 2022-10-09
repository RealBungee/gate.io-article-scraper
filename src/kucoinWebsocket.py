# !/usr/bin/env python
# coding: utf-8

import hashlib
import hmac
import json
import logging
import time
from websocket import WebSocketApp
#from bot import send_message
from webhook import send_kucoin_trade_alert
from webSocketQueue import getTicker

class KucoinWebSocketApp(WebSocketApp):

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
        if 'data' in message:
            pair = message['data']['symbol']
            amount = float(message['data']['size'])
            price = float(message['data']['price'])
            side = message['data']['side']
            dollar_amount = round(amount * price, 2)
            if side == 'buy' and dollar_amount > 1000:
                side = 'bought'
                content = f'```Someone {side} ${dollar_amount} of {pair} at {price}.```'
                if dollar_amount > 10000:
                    content += '@everyone'
                send_kucoin_trade_alert(content)
                #send_message(content)
            # else:
            #     side = 'sold'
            
    except Exception as e:
        logging.warning(e)
    logging.info("message received from server: {}".format(message))

def on_open(ws):
    logging.info('Starting kucoin websocket')
    subscribe = '/market/match:'
    for i in range(0, 100):
        ticker = getTicker()
        subscribe += ticker
        if i < 99:
            subscribe += ','
    ws.subscribe(subscribe)
