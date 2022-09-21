import csv
import logging
import sys
import json
import os
from time import sleep
from coingecko import get_all_futures_coins
from webhook import send_perp_listing_alert, send_perp_delisting_alert
sys.path.append('../gate.io-article-scraper')

#used to load the original config file
def load_scrapeData_file():
    f = open('./Data/coinData.json')
    data = json.load(f)
    coin_data = data['config']['scrapeData']
    print(coin_data)
    return coin_data

def load_twitter_accounts():
    f = open('./Data/twitterAccounts.txt')
    accounts = json.load(f)
    return accounts

def save_twitter_accounts(accounts):
    logging.info('Saving twitter account information to a json file')
    with open('./Data/twitterAccounts.txt', 'w') as file:
        file.write(json.dumps(accounts))

#save the latest released article number to csv file
def save_latest_article(article_number):
    myFile = open('./Data/latest_article.csv', 'w', newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(article_number)

#load the last article number scraped
def load_latest_article():
    article_num = ''
    with open('./Data/latest_article.csv', newline='') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            article_num = row
    return int(article_num[0])

# Saves list of tokens on exchange to ./ListingsData
# e.g save_object(list, "binance_futures")
def save_object(obj, exchangeName):
    try:
        with open("./Data/" + exchangeName + ".json", "w") as f:
            json.dump(obj, f)
    except Exception as ex:
        logging.error(f'Error saving json object: {ex}')

# Loads a stored list of tokens from ./ListingsData
# e.g load_object("binance_futures")
def load_object(filename):
    try:
        with open("./Data/"+ filename, "rb") as f:
            return json.load(f)
    except Exception as ex:
        logging.error(f'Error loading json object: {ex}')

# Compares the list of stored token listings to current listings then updates
def get_futures_listings():
    logging.info('Futures thread started')
    while(True):
        try:
            # Create listing file if it doesn't exist
            if not os.path.isfile("./Data/futuresCoins.json"):
                create_futures_listing_file()

            # load saved exchange data
            exchanges = load_object("futuresCoins.json")
            updatedExchanges = []
            removedListing = 0
            addedListing = 0
            
            # loop through each exchange and check for listings
            for item in exchanges:
                currentListings = get_all_futures_coins(item[0]['exchange'])
                updatedExchanges.append(currentListings)

                # Compare
                addedListing = [i for i in currentListings[0]['tickers'] if i not in item[0]['tickers']]
                removedListing = [i for i in item[0]['tickers'] if i not in currentListings[0]['tickers']]

                # Check for delist
                if len(removedListing) > 0:
                    for token in removedListing:
                        send_perp_delisting_alert(item[0]['name'], token['trade_url'], token['symbol'])
        
                # Check for listing
                if len(addedListing) > 0:
                    for token in addedListing:                    
                        send_perp_listing_alert(item[0]['name'], token['trade_url'], token['symbol'])
            
            # Update futuresCoins file
            save_object(updatedExchanges, "futuresCoins")
        
        except Exception as ex:
            logging.exception("Error during listing update:", ex)
        
        # Sleep thread for 60 seconds
        sleep(60)
        
# Create data file from selected exchanges in exchangList array
def create_futures_listing_file():
    # All wanted exchanges
    exchangesList = ["binance_futures", "ftx", "okex_swap",
     "mxc_futures", "gate_futures", "kumex",
     "bitmex", "huobi_dm", "kraken_futures"]
    
    listings = []
    
    for exchange in exchangesList:
        listings.append(get_all_futures_coins(exchange)) 
    
    save_object(listings, "futuresCoins")
