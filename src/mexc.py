import logging
import cloudscraper
from random import randint
from bs4 import BeautifulSoup
from time import sleep
from xmlrpc.client import ProtocolError
from http.client import RemoteDisconnected
from requests.exceptions import SSLError
from coingecko import get_coin_markets
from text_processing import get_mexc_coin, concat_markets
from webhook import send_mexc_article_alert, send_mexc_listing_alert

def initialize_articles(url, scraper):
    try:
        res = scraper.get(url)
        if res.status_code != 200: return []

        html = BeautifulSoup(res.text, 'html.parser')
        items = html.find_all('li', class_='article-list-item article-promoted')
        new_articles = []
        for i in items:
            article = i.find('a').text
            new_articles.append(article) 
        return new_articles
    except (RemoteDisconnected, ConnectionError, ProtocolError, SSLError, Exception) as e:
        logging.exception('Exception while scraping mexc: ', e)
        return []

def scrape_mexc(url, scraper, saved_articles):
    try:
        res = scraper.get(url)
        if res.status_code != 200: return []

        html = BeautifulSoup(res.text, 'html.parser')
        items = html.find_all('li', class_='article-list-item article-promoted')
        new_articles = []
        for i in items:
            article = i.find('a').text
            if article not in saved_articles:
                url = 'https://support.mexc.com/' + i.find('a').get('href')
                new_articles.append({ 'title': article, 'url': url})
        return new_articles
    except (RemoteDisconnected, ConnectionError, ProtocolError, SSLError, Exception) as e:
        logging.exception('Exception while scraping mexc: ', e)
        return []

def mexc():
    initialized = False
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
    listing_url = 'https://support.mexc.com/hc/en-001/sections/360000547811-New-Listings'
    news_url = 'https://support.mexc.com/hc/en-001/sections/360000679912-Latest-News'
    saved_listings = initialize_articles(listing_url, scraper)
    saved_news = initialize_articles(news_url, scraper)
    if len(saved_listings) > 1 and len(saved_news) > 1:
        logging.info('Initialized Mexc Listing and News Articles')
        initialized = True
    sleep(60)
    fetch_count = 0
    while(True):
        if len(saved_listings) < 1 or len(saved_news) < 1: 
            logging.warning('Released article list is empty...Setting initialized to false')
            initialized = False
        
        if initialized:
            new_articles = scrape_mexc(listing_url, scraper, saved_listings)
            for a in new_articles:
                saved_listings.append(a['title'])
                coin =  get_mexc_coin(a['title'])
                exchanges = concat_markets(get_coin_markets(coin))
                send_mexc_listing_alert(a['title'], a['url'], exchanges)
                logging.info('NEW LISTING ALERT')
            
            new_articles = scrape_mexc(news_url, scraper, saved_news)
            for a in new_articles:
                saved_news.append(a['title'])
                send_mexc_article_alert(a['title'], a['url'])
                logging.info('NEWS ALERT')
            fetch_count += 1
        if fetch_count >= 120 or not initialized:
            sleep(30)
            logging.warning('Re-initializing existing article list')
            saved_listings = initialize_articles(listing_url, scraper)
            saved_news = initialize_articles(news_url, scraper)
            if len(saved_listings) > 1 and len(saved_news) > 1:
                logging.info('Mexc articles re-initialized')
                initialized = True 
                fetch_count = 0
           
        sleep(randint(50, 80))