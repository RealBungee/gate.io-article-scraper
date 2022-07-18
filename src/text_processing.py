def get_coin_from_listing_title(title):
    coin = title.split('(')
    coin = coin[1].split(')')
    coin = coin[0].lower()
    return coin

def concat_markets(markets):
    if not 'No markets available' in markets:
        exchanges = '| '
        for m in markets:
            exchanges += m + ' | '
    else:
        exchanges = markets
    return exchanges