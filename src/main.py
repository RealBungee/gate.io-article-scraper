import logging
import threading
from time import sleep
from text_processing import get_coin_from_listing_title
from text_processing import get_coin_from_listing_title
from scraper import scrape_gateio_article, scrape_mexc_article
from coingecko import get_coin_markets
from webhook import send_gateio_article_alert, send_gateio_listing_alert, send_mexc_listing_alert
from storageMethods import update_futures_listings, save_latest_article, load_latest_article

def mexc():
    logging.info('Mexc scraper started')
    recent_articles = scrape_mexc_article(extended=True)
    logging.info('Successfully loaded most recent Mexc listings')
    while(True):
        article, url = scrape_mexc_article()
        if article not in recent_articles:
            send_mexc_listing_alert(article, url)
            recent_articles.insert(0, article)
            recent_articles.pop(len(recent_articles)-1)
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
                markets = get_coin_markets(get_coin_from_listing_title(title))
                send_gateio_listing_alert(title, content, link, markets)
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
    #futures = threading.Thread(target=check_for_futures_updates)

    logging.info('Starting threads')
    g.start()
    m.start()
    #futures.start()
    
main()