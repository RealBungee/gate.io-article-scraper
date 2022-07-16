import csv
import logging
import pickle
from coingecko import get_all_futures_coins
from webhook import send_perp_listing_alert, send_perp_delisting_alert

#save the latest released article number to csv file
def save_latest_article(article_number):
    myFile = open('latest_article.csv', 'w', newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(article_number)

#load the last article number scraped
def load_latest_article():
    article_num = ''
    with open('latest_article.csv', newline='') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            article_num = row
    return article_num[0]

# Saves list of tokens on exchange to ./ListingsData
# e.g save_object(list, "binance_futures")
def save_object(obj, exchangeName):
    try:
        with open("./ListingsData/" + exchangeName + ".pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        logging.error(f'Error during pickling object (Possibly unsupported): {ex}')

# Loads a stored list of tokens from ./ListingsData
# e.g load_object("binance_futures")
def load_object(filename):
    try:
        with open("./ListingsData/" + filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        logging.error(f'Error during unpickling object (Possibly unsupported): {ex}')

# Compares the list of stored token listings to current listings then updates
# e.g check_listing_updates("binance_futures")
def check_listing_updates(exchange):
    try:
        storedListings = load_object(exchange + ".pickle")
        currentListings = get_all_futures_coins(exchange)
        logging.info(f'Stored listings: {len(storedListings)}')
        logging.info(f'Current listings: {len(currentListings)}')

        # Compare
        removedListing = set(storedListings).difference(currentListings)
        addedListing = set(currentListings).difference(storedListings)
        
        # Update stored list 
        if len(removedListing) == 0 and len(addedListing) == 0: 
            logging.info(f'No perpetual updates!')

        if len(removedListing) > 0:
            # Alert for delist
            for token in removedListing:
                send_perp_delisting_alert(list(token)[0], list(token)[1])
                logging.info(f'Delisting alert!')
            save_object(currentListings, exchange)
        if len(addedListing) > 0:
            # Alert for listing
            for token in addedListing:
                send_perp_listing_alert(list(token)[0], list(token)[1])
                logging.info(f'Listing alert!')
            save_object(currentListings, exchange)
    except Exception as ex:
        logging.error(f'Error during listing update: {ex}')