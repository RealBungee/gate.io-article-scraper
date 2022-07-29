import logging
import threading
from time import sleep
from gate import gateio
from mexc import mexc
from twitter import twitter
from storageMethods import update_futures_listings

def check_for_futures_updates():
    logging.info('Futures thread started')
    while(True):
        try:
            logging.info('Checking for futures updates')
            update_futures_listings()
            sleep(60)
        except TypeError as err:
            logging.error(f'Error checking for listings: {err}')

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    g = threading.Thread(target=gateio)
    m = threading.Thread(target=mexc)
    t = threading.Thread(target=twitter)
    #futures = threading.Thread(target=check_for_futures_updates)

    logging.info('Starting threads')
    g.start()
    sleep(5)
    logging.info('Gate.io scraper started')
    m.start()
    sleep(30)
    logging.info('Mexc scraper started')
    t.start()
    #futures.start()
    
main()