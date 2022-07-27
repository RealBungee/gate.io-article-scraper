import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from text_processing import get_mexc_coin, concat_markets
from coingecko import get_coin_markets
from webhook import send_mexc_article_alert, send_mexc_listing_alert

def load_mexc_articles(link):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    sleep(5)

    try:
        articles = []
        for i in range(1, 11):
            title = driver.find_element(By.XPATH, f'/html[1]/body[1]/main[1]/div[2]/div[1]/section[1]/ul[1]/li[{i}]').text
            articles.append(title)
        logging.info('Successfully loaded most recent Mexc Listing Articles')
        return articles
    except (NoSuchElementException, WebDriverException) as ex:
        logging.exception(f'Error while loading recent Mexc articles: {ex}')

def scrape_mexc_listings(articles, link):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    sleep(5)

    try:
        new_article_list = []
        released_articles = []
        for i in range(1, 11):
            title = driver.find_element(By.XPATH, f'/html[1]/body[1]/main[1]/div[2]/div[1]/section[1]/ul[1]/li[{i}]').text
            if title not in articles:
                url = driver.find_element(By.XPATH, f'/html[1]/body[1]/main[1]/div[2]/div[1]/section[1]/ul[1]/li[{i}]/a[1]').get_attribute('href')
                released_articles.append({'title': title, 'url': url})
            new_article_list.append(title)
        return released_articles, new_article_list
    except (NoSuchElementException, WebDriverException) as ex:
        logging.exception(f'Error finding article: {ex}')
        return [], articles 

def mexc():
    listings_link = 'https://support.mexc.com/hc/en-001/sections/360000547811-New-Listings'
    news_link = 'https://support.mexc.com/hc/en-001/sections/360000679912-Latest-News'
    saved_listings =  load_mexc_articles(listings_link)
    saved_news = load_mexc_articles(news_link)
    while(True):
        released_articles, saved_listings = scrape_mexc_listings(saved_listings, listings_link)
        for a in released_articles:
            coin =  get_mexc_coin(a['title'])
            exchanges = concat_markets(get_coin_markets(coin))
            send_mexc_listing_alert(a['title'], a['url'], exchanges)
            logging.info('NEW LISTING ALERT')
        released_news, saved_news = scrape_mexc_listings(saved_news, news_link)
        for a in released_news:
            #coin = get_mexc_coin(a['title'])
            #exchanges = concat_markets(get_coin_markets(coin))
            send_mexc_article_alert(a['title'], a['url'])
            logging.info('NEWS ALERT')
        logging.info('Looking for News in 60 seconds')
        logging.info('Looking for new annoucements in 60 seconds')
        sleep(60)