from lib2to3.pgen2 import driver
import logging
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def scrape_gateio_article(article_number):
    article_link = f'https://www.gate.io/article/{article_number}'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-minimized")
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    #start the chrome driver (open browser)
    driver = webdriver.Chrome(options=options)
    driver.get(article_link)
    sleep(3)

    try:
        #detect wether article has been posted already
        try:
            title = driver.find_element(By.XPATH, '//h1[text() ="no article!"]')
            return title.text, article_link, ''
        except NoSuchElementException as err:
            logging.warning('Element containing "no article!" not found')

        try:
            title = driver.find_element(By.XPATH, '//body[text() ="not permitted"]')
            title = 'no article!'
            return title, article_link, ''
        except NoSuchElementException as err:
            logging.warning('Element containing "not permitted!" not found')

        try:
            article_title = driver.find_element(By.CLASS_NAME, 'dtl-title')
            title = article_title.find_element(By.XPATH, '//h1').text
            if 'Gate.io will list' in title:
                curr_year = str(date.today().year)
                main_content = driver.find_element(By.CLASS_NAME, 'dtl-content')
                content = main_content.text
                content = content.split(curr_year)
                content = content[0]
                return title, article_link, content
            return title, article_link, ''
        except NoSuchElementException as err:
            logging.warning('No title found', err)
    except WebDriverException as err:
        logging.warning(f'Error while trying to load article: \n{err}')
    driver.quit()

def scrape_mexc_article(extended = False):
    website_link = f'https://support.mexc.com/hc/en-001/sections/360000547811-New-Listings'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-minimized")
    #options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #start the chrome driver (open browser)
    driver = webdriver.Chrome(options=options)
    driver.get(website_link)
    sleep(3)

    if(extended):
        recent_articles = []
        for i in range(1, 6):
            try:
                title = driver.find_element(By.XPATH, f'/html[1]/body[1]/main[1]/div[2]/div[1]/section[1]/ul[1]/li[{i}]').text
                recent_articles.append(title)
            except (NoSuchElementException, WebDriverException) as ex:
                logging.exception(f'Error finding article: {ex}')
        return recent_articles
    else:
        #detect new articles
        try:
            title = driver.find_element(By.XPATH, f'/html[1]/body[1]/main[1]/div[2]/div[1]/section[1]/ul[1]/li[1]').text
            url = driver.find_element(By.XPATH, '/html[1]/body[1]/main[1]/div[2]/div[1]/section[1]/ul[1]/li[1]/a[1]').get_attribute('href')
            return title, url
        except (NoSuchElementException, WebDriverException) as ex:
            logging.exception(f'Error finding article: {ex}')