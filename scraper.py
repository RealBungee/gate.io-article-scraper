import logging

from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def check_for_article(article_number):
    article_link = f'https://www.gate.io/article/{article_number}'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-minimized")
    driver = webdriver.Chrome(options=options)
    driver.get(article_link)
    sleep(2)

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