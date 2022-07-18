import csv
import logging
import pickle
import os
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
        with open("../ListingsData/" + exchangeName + ".pickle", "wb") as f:
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
def update_futures_listings():
    try:
        # Create listing file if it doesn't exist
        if not os.path.isfile("./ListingsData/futuresListings.pickle"):
            create_futures_listing_file()
        # load saved exchange data
        exchanges = load_object("futuresListings.pickle")
        removedListing = 0
        addedListing = 0
        # loop through each exchange and check for listings
        for item in exchanges:
            currentListings = get_all_futures_coins(item[0][1])
            
            # Compare
            removedListing = [i for i in currentListings[0][2] if i not in item[0][2]]
            addedListing = [i for i in item[0][2] if i not in currentListings[0][2]]
            
            # Check for delist
            if len(removedListing) > 0:
                send_perp_delisting_alert(item[0][0], removedListing[0][0], removedListing[0][1])
                save_object(currentListings, "futuresListings")
            # Check for listing
            if len(addedListing) > 0:
                send_perp_listing_alert(item[0][0], removedListing[0][0], removedListing[0][1])
                save_object(currentListings, "futuresListings")
        if ((len(addedListing) + len(removedListing)) == 0):
            print("No futures listings or delistings found - retrying in 60 seconds")
    except Exception as ex:
        print("Error during listing update:", ex)
 
# Create data file from selected exchanges in exchangList array
def create_futures_listing_file():
    # All wanted exchanges
    exchangesList = ["binance_futures", "ftx", "okex_swap",
     "mxc_futures", "gate_futures", "kumex",
     "bitmex", "huobi_dm", "kraken_futures"]
    
    listings = []
    
    for exchange in exchangesList:
        listings.append(get_all_futures_coins(exchange)) 
    
    save_object(listings, "futuresListings")