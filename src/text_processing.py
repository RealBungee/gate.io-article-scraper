import logging


def get_coin_abbreviation(title):
    if '(' in title:
        coin = title.split('(')
        coin = coin[1].split(')')
        coin = coin[0].upper()
    return coin

def get_gate_coin(title):
    try:
        title = title.lower()
        if 'startup' in title:
            tmp = title.split(':')
            tmp = tmp[1].split('(')
            tmp = tmp[0]
            title = ''
        if '(' in title:
            tmp = title.split('will list ')
            tmp = tmp[1].split('(')
            tmp = tmp[0]
            title = ''
        tmp = tmp.split(' ')
        coin = ''
        for i, c in enumerate(tmp):
            if c != '':
                coin += c 
                if i != len(tmp):
                    coin += ' '
        logging.info(f'Extracted coin name: {coin} from title...')
        return coin
    except Exception as e:
        logging.error(f'Error extracting coin name from title: \n{e}')
        return ''

def get_mexc_coin(title):
    try:
        title = title.lower()
        if 'listing arrangement' in title:
            tmp = title.split('for')
            tmp = tmp[1].split('(')
            tmp = tmp[0]
            title = ''
        if '(' in title:
            if 'new m-day' in title:
                tmp = title.split('new m-day')
                tmp = tmp[1].split('(')
                tmp = tmp[0]
            elif 'trading contest' in title:
                tmp = title.split('trading contest with')
                tmp = tmp[1].split('(')
                tmp = tmp[0]
            elif 'contract swap' in title:
                tmp = title.split('the ')
                tmp = tmp[1].split('(')
                tmp = tmp[0]
            elif 'resumption' in title:
                tmp = title.split('for ')
                tmp = tmp[1].split('(')
                tmp = tmp[0]
            else:
                tmp = title.split('will list')
                tmp = tmp[1].split('(')
                tmp = tmp[0]
            title = ''
        elif '-' in title:
            tmp = title.split('-')
            tmp = tmp[1].split('in the')
            tmp = tmp[0]
        else:
            tmp = ''
        tmp.split(' ')
        coin = ''
        for i, c in enumerate(tmp):
            if c != '':
                coin += c 
                if i != len(tmp):
                    coin += ' '
        logging.info(f'Extracted coin name: {coin} from {title}')
        return coin
    except Exception as e:
        logging.error(f'Error extracting coin from title: \n{e}')


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