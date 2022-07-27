def get_coin_abbreviation(title):
    if '(' in title:
        coin = title.split('(')
        coin = coin[1].split(')')
        coin = coin[0].upper()
    return coin

def get_gate_coin(title):
    title = title.lower()
    if 'startup' in title:
        coin = title.split(':')
        coin = coin[1].split('(')
        if 'coin' in coin[0]:
            coin  = coin[0].replace(' ', '')
        else:
            coin = coin[0]
        title = ''
    if '(' in title:
        coin = title.split('will list ')
        coin = coin[1].split('(')
        coin = coin[0]
        title = ''
    if ' ' in coin[0]:
        coin = coin.replace(' ', '')
    print(coin)
    return coin

def get_mexc_coin(title):
    title = title.lower()
    if 'listing arrangement' in title:
        coin = title.split('for')
        coin = coin[1].split('(')
        coin = coin[0]
        title = ''
    elif '(' in title:
        if 'new m-day' in title:
            coin = title.split('new m-day')
            coin = coin[1].split('(')
            coin = coin[0]
        else:
            coin = title.split('will list')
            coin = coin[1].split('(')
            coin = coin[0]
        title = ''
    elif '-' in title:
        coin = title.split('-')
        coin = coin[1].split('in the')
        coin = coin[0]
    else:
        coin = ''
    coin = coin.replace(' ', '')
    print(coin)
    return coin


def concat_markets(markets):
    if markets == '':
        return 'No markets available'

    if not 'No markets available' in markets:
        exchanges = '| '
        for m in markets:
            exchanges += m + ' | '
    else:
        exchanges = markets
    return exchanges