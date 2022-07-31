import logging
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from storageMethods import load_latest_article, save_latest_article
from text_processing import get_coin_abbreviation, get_gate_coin, concat_markets
from coingecko import get_coin_markets
from webhook import send_gateio_article_alert, send_gateio_listing_alert

# def scrape_gateio_article(article_number):
#     article_link = f'https://www.gate.io/article/{article_number}'
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
#     #start the chrome driver (open browser)
#     driver = webdriver.Chrome(options=options)
#     driver.get(article_link)
#     sleep(3)

#     #detect whether the article is not posted yet
#     try:
#         title = driver.find_element(By.XPATH, '//h1[text() ="no article!"]')
#         return '', '', ''
#     except (NoSuchElementException, WebDriverException) as err:
#         logging.warning('Element containing "no article!" not found')
#     #detect whether the article is not posted yet
#     try:
#         title = driver.find_element(By.XPATH, '//body[text() ="not permitted"]')
#         return '', '', ''
#     except (NoSuchElementException, WebDriverException) as err:
#         logging.warning('Element containing "not permitted!" not found')

#     #detect what article has been posted and its contents
#     try:
#         title = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/h1[1]').text
#         if 'Sale Result' in title:
#             coin = get_coin_abbreviation(title)
#             main_content = driver.find_element(By.XPATH, f'//span[contains(text(),"We will commence {coin} trading")]')
#             content = main_content.text.split('.')
#             content = content[0]
#             return title, article_link, content

#         if 'Gate.io Startup Free Offering:' in title or 'Gate.io Startup:' in title or 'Initial Free Offering:' in title:
#             coin = get_coin_abbreviation(title)
#             main_content = driver.find_element(By.XPATH, f'//div[@class="dtl-content"]')
#             content = main_content.text.split('(2) ')
#             content = content[1].split(',')
#             content = content[0]
#             return title, article_link, content

#         if 'Gate.io will list' in title:
#             curr_year = str(date.today().year)
#             main_content = driver.find_element(By.CLASS_NAME, 'dtl-content')
#             content = main_content.text.split(curr_year)
#             content = content[0]
#             return title, article_link, content

#         return title, article_link, ''
#     except (NoSuchElementException, WebDriverException, Exception) as err:
#         logging.warning('No title found', err)
#         driver.quit()
#         return '', '', ''

def get_article(url):
    headers = {
        "cookie": "lang=en; curr_fiat=USD; market_title=usdt; defaultBuyCryptoFiat=EUR; _ga=GA1.2.1735262583.1657554676; _uetvid=cbee6840050911ed93dd19846032d0f6; b_notify=1; notify_close=kyc; show_zero_funds=1; chatroom_lang=en; idb=1658613657; futureRisktip=1; show_tv=1; _gid=GA1.2.972110085.1659160898; login_notice_check=^%^2F; countryId_leftbar=78; last_lang_leftbar=en; ch=ann27383; l_d_data_USDT_time=1659198495917; lasturl=^%^2Farticle^%^2F27373; AWSALB=8xysfLpDMUMKCDm+ke+gsAcWji76Yv0S1a7MZ/7M5oz9wEHbSHmpa5rYm9ULieQEcQtxJOuytuYLx8Xcqz7WNIxtqm1lnbMdLb6rU/FHQgdoFxCYd9PaX6MNMHWG; AWSALBCORS=8xysfLpDMUMKCDm+ke+gsAcWji76Yv0S1a7MZ/7M5oz9wEHbSHmpa5rYm9ULieQEcQtxJOuytuYLx8Xcqz7WNIxtqm1lnbMdLb6rU/FHQgdoFxCYd9PaX6MNMHWG",
        "authority": "www.gate.io",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9,hr;q=0.8,bs;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "^\^.Not/A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    try:
        return requests.request("GET", url, headers=headers)
    except Exception as e:
        logging.exception(f'Exception occured while fetching gateio article: \n{e}')

def scrape_gateio(article_number):
    url = f'https://www.gate.io/article/{article_number}'
    response = get_article(url)
    html = BeautifulSoup(response.content, 'html.parser')
    if response.status_code != 200: return {'title':  '', 'url': '', 'content': ''}
    
    title = html.select('h1')[0].text
    content = html.find('div', class_='dtl-content')
    if title == 'not permitted' or 'no article!' in title : return {'title':  '', 'url': '', 'content': ''}
    
    try:
        if 'Sale Result' in title:
            coin = get_coin_abbreviation(title)
            content = content.find_all('span')
            for c in content:
                if f'We will commence {coin} trading' in c.text:
                    content = c.text
                    break
            content = content.split('.')
            content = content[0]
            return title, url, content

        if 'Gate.io Startup Free Offering:' in title or 'Gate.io Startup:' in title or 'Initial Free Offering:' in title:
            coin = get_coin_abbreviation(title)
            content = content.find_all('br')
            for c in content:
                if f'Trading starts' in c.text:
                    content = c.text
                    break
            content = content.split('Trading starts ')
            content = content[1].split(',')
            content = 'Trading starts ' + content[0]
            return title, url, content

        if 'Gate.io will list' in title:
            content = content.find_all('strong')
            content = content[0].text
            return title, url, content
    except Exception as e:
        logging.exception(f'Exception while scraping gateio: \n{e}')
        return {'title':  '', 'url': '', 'content': ''}

def gateio():
    article_number = int(load_latest_article())
    times_checked = 0
    while(True):
        if times_checked >= 5:
            logging.info('Checking next article in case current was deleted...')
            times_checked = 0
            temp_article = article_number + 1
            article = scrape_gateio(temp_article)
        else:
            article = scrape_gateio(article_number)
        
        if article['title'] == '':
            logging.info('No new listing announcements found - retrying in 60 seconds')
            times_checked += 1
            sleep(60)
        else:
            if article['content'] == '':
                send_gateio_article_alert(article['title'], ['link'])
                logging.info('NEW ARTICLE ALERT!')
            else:
                exchanges = concat_markets(get_coin_markets(get_gate_coin(article['title'])))
                send_gateio_listing_alert(article, exchanges)
                logging.info('NEW LISTING ALERT!')
            if times_checked >= 5:
                article_number += 2
            else:
                article_number += 1
            save_latest_article([article_number])
            times_checked = 0
            sleep(5)