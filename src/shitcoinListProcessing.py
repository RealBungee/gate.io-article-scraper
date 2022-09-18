import json
import coingecko
from gateAPI import get_gateio_listed_coins
from kucoin import get_listed_coins

#first step is to update the list with most recent data and most recent shitcoins from coingecko
def save_coins_market_data():
    res = coingecko.get_coins_market_data()
    with open('./Data/allCoingeckoShitcoins.json', 'w') as file:
        file.write(json.dumps(res))

def load_coins_market_data():
    f = open('./Data/allCoingeckoShitcoins.json')
    return json.load(f)

#combine the lists of coins listed on Exchanges (for now Gateio and Kucoin)...
def get_all_listed_coins():
    kucoin_coins = get_listed_coins()
    gateio_coins = get_gateio_listed_coins()
    return list(set(kucoin_coins + gateio_coins))

def remove_margin_tokens(list):
    for index, c in enumerate(list):
        if '3L' in c or '3S' in c:
            list.pop(index)
    return list

def filter_coins_by_mc(coin_market_data):
    ignored_ids = []
    ignored_symbols = ['jasmy','undead', 'ape', 'xrp', 'waves']
    shitcoins = []
    low_caps = []
    for c in coin_market_data:
        try:
            coin = {'id': c['id'], 'symbol': c['symbol'], 'name': c['name'], 'market_cap': c['market_cap']}
            if 'peg' not in c['id'] and 'wormhole' not in c['id'] and 'wrapped' not in c['id'] and c['symbol'] not in ignored_symbols and c['symbol'].upper() in listed_coins and c['market_cap'] != None:
                if  c['market_cap'] < 250000000:
                    shitcoins.append(coin)
                if  c['market_cap'] >= 250000000 and c['market_cap'] < 1500000000:
                    low_caps.append(coin)
        except KeyError as e:
            print(f'Error: {e}')
    with open('./Data/shitcoins.json', 'w') as f:
        f.write(json.dumps(shitcoins))
    with open('./Data/lowCaps.json', 'w') as f:
        f.write(json.dumps(low_caps))
    return shitcoins, low_caps    

#save_coins_market_data()
coin_market_data = load_coins_market_data()
listed_coins = get_all_listed_coins()
listed_coins = remove_margin_tokens(listed_coins)
shitcoins, _ = filter_coins_by_mc(coin_market_data)
print(len(shitcoins))