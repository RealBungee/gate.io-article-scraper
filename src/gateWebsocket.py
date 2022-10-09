# !/usr/bin/env python
# coding: utf-8

import hashlib
import hmac
import json
import logging
import time
from websocket import WebSocketApp
from webhook import send_gateio_trade_alert

class GateWebSocketApp(WebSocketApp):

    def __init__(self, url, api_key, api_secret, **kwargs):
        super(GateWebSocketApp, self).__init__(url, **kwargs)
        self._api_key = api_key
        self._api_secret = api_secret

    def _send_ping(self, interval, event):
        while not event.wait(interval):
            self.last_ping_tm = time.time()
            if self.sock:
                try:
                    self.sock.ping()
                except Exception as ex:
                    logging.warning("send_ping routine terminated: {}".format(ex))
                    break
                try:
                    self._request("spot.ping", auth_required=False)
                except Exception as e:
                    raise e

    def _request(self, channel, event=None, payload=None, auth_required=True):
        current_time = int(time.time())
        data = {
            "time": current_time,
            "channel": channel,
            "event": event,
            "payload": payload,
        }
        if auth_required:
            message = 'channel=%s&event=%s&time=%d' % (channel, event, current_time)
            data['auth'] = {
                "method": "api_key",
                "KEY": self._api_key,
                "SIGN": self.get_sign(message),
            }
        data = json.dumps(data)
        logging.info('request: %s', data)
        self.send(data)

    def get_sign(self, message):
        h = hmac.new(self._api_secret.encode("utf8"), message.encode("utf8"), hashlib.sha512)
        return h.hexdigest()

    def subscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "subscribe", payload, auth_required)

    def unsubscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "unsubscribe", payload, auth_required)


def on_message(ws, message):
    # type: (GateWebSocketApp, str) -> None
    # handle whatever message you received
    message = json.loads(message)
    #logging.info("message received from server: {}".format(message))
    try:
        if message['event'] == 'update' and 'currency_pair' in message['result']:
            pair = message['result']['currency_pair']
            amount = float(message['result']['amount'])
            price = float(message['result']['price'])
            side = message['result']['side']
            dollar_amount = round(amount * price, 2)
            if side == 'buy' and dollar_amount > 1000:
                side = 'bought'
                content = f'```Someone {side} ${dollar_amount} of {pair} at {price}.```'
                if dollar_amount > 10000:
                    content += '@everyone'
                send_gateio_trade_alert(content)
            # else:
            #     side = 'sold'
    except Exception as e:
        logging.warning(e)

def on_open(ws):
    # type: (GateWebSocketApp) -> None
    # subscribe to channels interested
    logging.info('websocket connected')
    f = open('./Data/shitcoins.json')
    coins = json.load(f)
    for c in coins:
        ticker = c['symbol'].upper() + '_USDT'
        ws.subscribe("spot.trades", [ticker], False)