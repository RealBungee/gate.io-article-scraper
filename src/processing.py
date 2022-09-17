from coingecko import get_coins_market_data

res = get_coins_market_data()

print(res)
print(len(res))