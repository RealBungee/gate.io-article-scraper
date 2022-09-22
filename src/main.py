import logging
import threading
from mexcAPI import mexc_listings
from kucoin import kucoin, start_kucoin_websocket
from gate import gateio, start_gateio_websocket
from futures import get_futures_listings

def main():
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    g = threading.Thread(target=gateio)
    m = threading.Thread(target=mexc_listings)
    k = threading.Thread(target=kucoin)
    gw = threading.Thread(target=start_gateio_websocket)
    kw = threading.Thread(target=start_kucoin_websocket)
    f = threading.Thread(target=get_futures_listings)

    logging.info('Starting threads')
    g.start()
    k.start()
    m.start()
    gw.start()
    kw.start()
    f.start()
    
main()