import logging
import threading
from time import sleep
from mexc import mexc
from kucoin import kucoin, start_kucoin_websocket
from gate import gateio, start_gateio_websocket
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
    k = threading.Thread(target=kucoin)
    gw = threading.Thread(target=start_gateio_websocket)
    kw = threading.Thread(target=start_kucoin_websocket)
    futures = threading.Thread(target=check_for_futures_updates)

    logging.info('Starting threads')
    g.start()
    k.start()
    m.start()
    futures.start()
    gw.start()
    kw.start()
    
main()