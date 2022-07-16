import logging
import threading
from time import sleep
from text_processing import get_coin_from_listing_title
from text_processing import get_coin_from_listing_title
from scraper import check_for_article
from coingecko import get_coin_markets
from webhook import send_new_article_alert, send_listing_alert
from storageMethods import check_listing_updates, save_latest_article, load_latest_article

def scrape_gate_articles():
    logging.info('Gate.io scraper thread started')
    article_number = int(load_latest_article())
    while(True):
        try:
            title, link, content = check_for_article(article_number)
        except TypeError as err:
            logging.error(f'Error checking for articles: {err}')
        
        if not("no article!" in title):
            if content != '':
                markets = get_coin_markets(get_coin_from_listing_title(title))
                send_listing_alert(title, content, link, markets)
                logging.info('NEW LISTING ALERT!')
            else:
                send_new_article_alert(title, link)
                logging.info('NEW ARTICLE ALERT!')
            article_number += 1
            save_latest_article([article_number])
            sleep(5)
        else:
            logging.info('Article not found - checking again in 60 seconds')
            sleep(60)

def check_for_futures_updates():
    logging.info('Futures thread started')
    while(True):
        try:
            logging.info('-----------------------------')
            logging.info('Checking for futures updates')
            check_listing_updates("binance_futures")
            sleep(60)
        except TypeError as err:
            logging.error(f'Error checking for listings: {err}')


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    
    logging.info('Creating threads')
    gate = threading.Thread(target=scrape_gate_articles)
    futures = threading.Thread(target=check_for_futures_updates)

    logging.info('Starting threads')
    gate.start()
    futures.start()
    
main()