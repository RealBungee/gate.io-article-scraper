import logging
import threading
from time import sleep
from text_processing import concat_markets, get_gate_coin, get_mexc_coin
from scraper import scrape_gateio_article, scrape_mexc_article, load_recent_mexc_articles
from coingecko import get_coin_markets
from twitter import get_tweets
from webhook import send_gateio_article_alert, send_gateio_listing_alert, send_mexc_listing_alert, send_tweet_alert
from storageMethods import update_futures_listings, save_latest_article, load_latest_article, save_twitter_accounts

def twitter():
    logging.info('Starting twitter terminal')
    # load information into an array or a map
    [1289071298556170240, 1256716686]
    accounts = [{'user_id': 1304552437487939585, 'latest_tweet': 1550003741197221888}, {'user_id':1289071298556170240, 'latest_tweet': 1525110032895025154}]
    initialized = False
    while(True):
        for a in accounts:
            res = get_tweets(a['user_id'], a['latest_tweet'])
            if res['meta']['result_count'] != 0:
                username = res['includes']['users'][0]['username']
                for t in res['data']:
                    tweet_id = t['id']
                    url = 'https://twitter.com/{}/status/{}'.format(username, tweet_id)
                    if initialized: send_tweet_alert(username, url)
                    a['latest_tweet'] = tweet_id
        if not initialized: initialized = True
        save_twitter_accounts(accounts)
        #save the most recent tweets to file
        sleep(10)   

def mexc():
    logging.info('Mexc scraper started')
    saved_articles = load_recent_mexc_articles()
    while(True):
        released_articles, saved_articles = scrape_mexc_article(saved_articles)
        for a in released_articles:
            exchanges = concat_markets(get_coin_markets(get_mexc_coin(a[0])))
            send_mexc_listing_alert(a[0], a[1], exchanges)
            logging.info('NEW LISTING ALERT')
        else:
            logging.info('No new listing announcements found - retrying in 30 seconds')
        sleep(30)

def gateio():
    logging.info('Gate.io scraper started')
    article_number = int(load_latest_article())
    while(True):
        try:
            title, link, content = scrape_gateio_article(article_number)
        except TypeError as err:
            logging.error(f'Error checking for articles: {err}')
        
        if not("no article!" in title):
            if content != '':
                exchanges = concat_markets(get_coin_markets(get_gate_coin(title)))
                send_gateio_listing_alert(title, content, link, exchanges)
                logging.info('NEW LISTING ALERT!')
            else:
                send_gateio_article_alert(title, link)
                logging.info('NEW ARTICLE ALERT!')
            article_number += 1
            save_latest_article([article_number])
            sleep(5)
        else:
            logging.info('No new listing announcements found - retrying in 60 seconds')
            sleep(60)

def check_for_futures_updates():
    logging.info('Futures thread started')
    while(True):
        try:
            logging.info('-----------------------------')
            logging.info('Checking for futures updates')
            update_futures_listings()
            sleep(60)
        except TypeError as err:
            logging.error(f'Error checking for listings: {err}')


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    
    logging.info('Creating threads')
    g = threading.Thread(target=gateio)
    m = threading.Thread(target=mexc)
    #t = threading.Thread(target=twitter)
    futures = threading.Thread(target=check_for_futures_updates)

    logging.info('Starting threads')
    g.start()
    m.start()
    #t.start()
    #futures.start()
    
main()