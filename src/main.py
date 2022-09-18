import logging
import threading
from mexc import mexc
from kucoin import kucoin, start_kucoin_websocket
from gate import gateio, start_gateio_websocket
from futures import check_for_futures_updates

def main():
    #filename='gateWebsocketLog.txt',filemode='a',
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    g = threading.Thread(target=gateio)
    m = threading.Thread(target=mexc)
    k = threading.Thread(target=kucoin)
    kw = threading.Thread(target=start_kucoin_websocket)
    gw = threading.Thread(target=start_gateio_websocket)
    futures = threading.Thread(target=check_for_futures_updates)

    logging.info('Starting threads')
    g.start()
    k.start()
    #m.start()
    gw.start()
    kw.start()
    futures.start()
    
main()