import logging
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from storageMethods import load_latest_article, save_latest_article
from text_processing import get_coin_abbreviation, get_gate_coin, concat_markets
from coingecko import get_coin_markets
from webhook import send_gateio_article_alert, send_gateio_listing_alert

def scrape_gateio_article(article_number):
    article_link = f'https://www.gate.io/article/{article_number}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    #start the chrome driver (open browser)
    driver = webdriver.Chrome(options=options)
    driver.get(article_link)
    sleep(3)

    #detect whether the article is not posted yet
    try:
        title = driver.find_element(By.XPATH, '//h1[text() ="no article!"]')
        return '', '', ''
    except (NoSuchElementException, WebDriverException) as err:
        logging.warning('Element containing "no article!" not found')
    #detect whether the article is not posted yet
    try:
        title = driver.find_element(By.XPATH, '//body[text() ="not permitted"]')
        return '', '', ''
    except (NoSuchElementException, WebDriverException) as err:
        logging.warning('Element containing "not permitted!" not found')

    #detect what article has been posted and its contents
    try:
        title = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/h1[1]').text
        if 'Gate.io Startup Free Offering:' in title:
            coin = get_coin_abbreviation(title)
            main_content = driver.find_element(By.XPATH, f'//div[@class="dtl-content"]')
            content = main_content.text.split('(2)')
            content = content[1].split(',')
            content = content[0]
            return title, article_link, content
        
        if 'Sale Result' in title or 'Gate.io Startup:' in title:
            coin = get_coin_abbreviation(title)
            main_content = driver.find_element(By.XPATH, f'//span[contains(text(),"We will commence {coin} trading")]')
            content = main_content.text.split('.')
            content = content[0]
            return title, article_link, content

        if 'Gate.io will list' in title:
            curr_year = str(date.today().year)
            main_content = driver.find_element(By.CLASS_NAME, 'dtl-content')
            content = main_content.text.split(curr_year)
            content = content[0]
            return title, article_link, content

        return title, article_link, ''
    except (NoSuchElementException, WebDriverException, Exception) as err:
        logging.warning('No title found', err)
        driver.quit()
        return '', '', ''

def gateio(article_number = 0, times_checked = 0):
    if article_number == 0:
        article_number = int(load_latest_article())
    
    if times_checked >= 10:
        logging.info('Checking next article in case current was deleted...')
        times_checked = 0
        temp_article = article_number + 1
        title, link, content = scrape_gateio_article(temp_article)
    else:
        title, link, content = scrape_gateio_article(article_number)
    
    if title == '':
        logging.info('No new listing announcements found - retrying in 60 seconds')
        times_checked += 1
        sleep(60)
    else:
        if content == '':
            send_gateio_article_alert(title, link)
            logging.info('NEW ARTICLE ALERT!')
        else:
            exchanges = concat_markets(get_coin_markets(get_gate_coin(title)))
            send_gateio_listing_alert(title, content, link, exchanges)
            logging.info('NEW LISTING ALERT!')
        if times_checked >= 10:
            article_number += 2
        else:
            article_number += 1
        save_latest_article([article_number])
        times_checked = 0
        sleep(5)
    gateio(article_number, times_checked)