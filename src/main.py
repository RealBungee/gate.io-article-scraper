import asyncio
import logging
import threading
from time import sleep
from bot import run_bot, send_message
from mexcAPI import mexc_listings
from kucoin import kucoin, start_kucoin_websocket
from gate import gateio, start_gateio_websocket
from futures import get_futures_listings

async def main():
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    #loop = asyncio.new_event_loop()
    g = threading.Thread(target=gateio)
    m = threading.Thread(target=mexc_listings)
    k = threading.Thread(target=kucoin)
    gw = threading.Thread(target=start_gateio_websocket)
    kw = threading.Thread(target=start_kucoin_websocket)
    f = threading.Thread(target=get_futures_listings)
    #discord_bot  = threading.Thread(target=run_bot, args=(loop,))

    logging.info('Starting threads')
    #discord_bot.start()
    #sleep(6)
    g.start()
    k.start()
    m.start()
    gw.start()
    kw.start()
    f.start()
    
asyncio.run(main())
#main()

