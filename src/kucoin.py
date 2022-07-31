import logging
import requests
import random
import time
import string
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from text_processing import get_mexc_coin, concat_markets
from coingecko import get_coin_markets
from webhook import send_kucoin_listing_alert

def scrape_listings(link, articles=[], initialized=False):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    sleep(5)

    try:
        new_article_list = []
        listings = []
        for i in range(1, 11):
            title = driver.find_element(By.XPATH, f'/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[{i}]/div[1]/div[2]/div[1]/span[1]').text
            if title not in articles and initialized:
                url = driver.find_element(By.XPATH, f'/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[{i}]').get_attribute('href')
                listings.append({'title': title, 'url': url})
            new_article_list.append(title)
        driver.quit()
        return listings, new_article_list
    except (NoSuchElementException, WebDriverException, Exception) as ex:
        logging.exception(f'Error finding article: {ex}')
        driver.quit()
        return [], articles 

def kucoin():
    listings_link = 'https://www.kucoin.com/news/categories/listing'
    initialized = False
    saved_listings = scrape_listings(listings_link, initialized=initialized)
    while(True):
        released_articles, saved_listings = scrape_listings(listings_link, saved_listings, initialized)
        if not initialized: initialized = True
        for a in released_articles:
            try:
                coin =  get_mexc_coin(a['title'])
            except IndexError as err:
                print('Index error: ', err)
            exchanges = concat_markets(get_coin_markets(coin))
            send_kucoin_listing_alert(a['title'], a['url'], exchanges)
            logging.info('NEW LISTING ALERT')
        logging.info('Looking for News in 60 seconds')
        logging.info('Looking for new annoucements in 60 seconds')
        sleep(60)


def get_kucoin_announcement():
    """
    Retrieves new coin listing announcements from Kucoin
    """
    logging.debug("Pulling announcement page")
    # Generate random query/params to help prevent caching
    rand_page_size = random.randint(1, 200)
    letters = string.ascii_letters
    random_string = "".join(random.choice(letters) for i in range(random.randint(10, 20)))
    random_number = random.randint(1, 99999999999999999999)
    queries = [
        "page=1",
        f"pageSize={str(rand_page_size)}",
        "category=listing",
        "lang=en_US",
        f"rnd={str(time.time())}",
        f"{random_string}={str(random_number)}",
    ]
    random.shuffle(queries)
    logging.debug(f"Queries: {queries}")
    request_url = (
        f"https://www.kucoin.com/_api/cms/articles?"
        f"?{queries[0]}&{queries[1]}&{queries[2]}&{queries[3]}&{queries[4]}&{queries[5]}"
    )
    latest_announcement = requests.get(request_url)
    if latest_announcement.status_code == 200:
        try:
            logging.debug(f'X-Cache: {latest_announcement.headers["X-Cache"]}')
        except KeyError:
            # No X-Cache header was found - great news, we're hitting the source.
            pass

        latest_announcement = latest_announcement.json()
        logging.debug("Finished pulling announcement page")
        print(latest_announcement["items"][0]["title"])
        return latest_announcement["items"][0]["title"]
    else:
        logging.error(f"Error pulling kucoin announcement page: {latest_announcement.status_code}")
        return ""
