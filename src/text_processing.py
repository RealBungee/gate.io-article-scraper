import logging

def concat_markets(markets):
    if markets == '' or markets == 'No markets available': return 'No markets available'

    exchanges = '| '
    for m in markets:
        exchanges += m + ' | '
    
    return exchanges

def get_coin_abbreviation(title):
    if '(' in title:
        coin = title.split('(')
        coin = coin[1].split(')')
        coin = coin[0].upper()
    return coin

def remove_spaces(text):
    res = text.split(' ')
    str = ''
    for i, r in enumerate(res):
        if r != '':
            str += r 
            if (i + 1 < len(res)) and res[i + 1] != '':
                str += ' '
    str = str.split(' ')
    if 'coin' in str[-1]:
        str[-1] = ''
    coin = ''
    for i, r in enumerate(str):
        if r != '':
            coin += r 
            if (i + 1 < len(str)) and str[i + 1] != '':
                coin += ' '
    return coin

def get_gate_coin(title):
    try:
        title = title.lower()
        if 'startup' in title:
            tmp = title.split(':')
            tmp = tmp[1].split('(')
            tmp = tmp[0]
        elif '(' in title:
            tmp = title.split('will list ')
            tmp = tmp[1].split('(')
            tmp = tmp[0]
        coin = remove_spaces(tmp)
        logging.info(f'Extracted coin name: {coin} from title: {title}')
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
        elif '(' in title:
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
        elif '-' in title:
            tmp = title.split('-')
            tmp = tmp[1].split('in the')
            tmp = tmp[0]
        else:
            tmp = ''
        coin = remove_spaces(tmp)
        logging.warning(f'Extracted coin name: {coin} from {title}')
        return coin
    except Exception as e:
        logging.error(f'Error extracting coin from title: \n{e}')