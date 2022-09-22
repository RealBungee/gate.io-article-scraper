import json
import logging
from webbrowser import get
import requests
from time import sleep
from random import randint
from webhook import send_mexc_beta_listing_alert

def save_list(obj, listName):
    try:
        with open("./Data/" + listName + ".json", "w") as f:
            json.dump(obj, f)
    except Exception as ex:
        print(ex)

def load_list(listName):
    try:
        with open("./Data/" + listName + ".json", "rb") as f:
            data = json.load(f)
        return data
    except Exception as ex:
        print(ex)

def get_listed_tokens():
    url = 'https://api.mexc.com/api/v3/exchangeInfo'
    res = requests.get(url = url).json().get('symbols')
    return filter_list_to_usdt_pairs(res)

def filter_list_to_usdt_pairs(coin_list):
    list_of_substrings = ['2L', '2S', '3S', '3L', '4L', '4S', '5L', '5S']
    coin_list = list(filter(lambda coin: coin['quoteAsset']=='USDT', coin_list))
    coins = [coin['symbol'] for coin in coin_list]
    filtered_coins = list(filter(lambda coin: not any(substring in coin for substring in list_of_substrings), coins))
    return filtered_coins 

def notify_new_listings(new_coins):
    base_url = "https://www.mexc.com/exchange/"
    for coin in new_coins:
        symbol = coin.replace('USDT', '') + '_USDT'
        url = base_url + symbol
        send_mexc_beta_listing_alert(f'New Coin Listing: {coin}\n{url}')
        logging.warning("New coin listing detected")

def mexc_listings():
    #initialize the pair list
    listed_coins = get_listed_tokens()
    #start an infinite loop to detect any new coin additions
    while(True):
        new_list = get_listed_tokens()
        new_coins = [x for x in new_list if x not in listed_coins]
        listed_coins += new_coins
        notify_new_listings(new_coins)
        sleep(randint(10, 20))