def get_coin_from_listing_title(title):
    coin = title.split('list ')
    coin = coin[1].split('(')
    coin = coin[0].lower()
    print(coin)
    return coin