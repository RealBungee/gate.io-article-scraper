def get_coin_from_listing_title(title):
    title = title.lower()
    if 'startup' in title:
        coin = title.split(':')
        coin = coin[1].split('(')
        coin = coin[0]
        title = ''
    if '(' in title:
        coin = title.split('will list')
        coin = coin[1].split('(')
        coin = coin[0]
        title = ''
    if '-' in title:
        coin = title.split('-')
        coin = coin[1].split('in the')
        coin = coin[0]
    coin = coin.replace(' ', '')
    print(coin)
    return coin

def concat_markets(markets):
    if not 'No markets available' in markets:
        exchanges = '| '
        for m in markets:
            exchanges += m + ' | '
    else:
        exchanges = markets
    return exchanges