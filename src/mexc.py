import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from text_processing import get_mexc_coin, concat_markets
from coingecko import get_coin_markets
from webhook import send_mexc_listing_alert

def load_recent_mexc_articles():
    website_link = f'https://support.mexc.com/hc/en-001/sections/360000547811-New-Listings'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(website_link)
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

def scrape_mexc_article(articles):
    website_link = f'https://support.mexc.com/hc/en-001/sections/360000547811-New-Listings'
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(website_link)
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

def mexc():
    saved_articles = load_recent_mexc_articles()
    while(True):
        released_articles, saved_articles = scrape_mexc_article(saved_articles)
        for a in released_articles:
            coin =  get_mexc_coin(a['title'])
            exchanges = concat_markets(get_coin_markets(coin))
            send_mexc_listing_alert(a['title'], a['url'], exchanges)
            logging.info('NEW LISTING ALERT')
        logging.info('Looking for new annoucements in 30 seconds')
        sleep(30)