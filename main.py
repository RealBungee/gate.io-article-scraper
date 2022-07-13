import csv
import logging
from time import sleep
from scraper import check_for_article
from webhook import send_new_article_alert, send_listing_alert
from coingecko import get_get_coin_markets

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def save_latest_article(article_number):
    myFile = open('latest_article.csv', 'w', newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(article_number)

def load_latest_article():
    article_num = ''
    with open('latest_article.csv', newline='') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            article_num = row
    return article_num[0]

def get_coin(title):
    coin = title.split('list ')
    coin = coin[1].split('(')
    coin = coin[0].lower()
    print(coin)
    return coin

def main():
    markets = ''
    article_number = int(load_latest_article())
    while(True):
        try:
            title, link, content = check_for_article(article_number)
            if not("no article!" in title):
                if content != '':
                    markets = get_get_coin_markets(get_coin(title))
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
        except TypeError as err:
            logging.error(f'Error checking for articles: {err}')
        
main()