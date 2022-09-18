import logging
import requests
from random import randint
from h11 import ProtocolError
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from http.client import RemoteDisconnected
from gateWebsocket import GateWebSocketApp, on_message, on_open
from text_processing import get_coin_abbreviation, get_gate_coin, concat_markets
from coingecko import get_coin_markets
from webhook import send_gateio_article_alert, send_gateio_listing_alert

def scrape_gateio_article(article_number):
    url = f'https://www.gate.io/article/{article_number}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    #start the chrome driver (open browser)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(3)

    #detect whether the article is not posted yet
    try:
        title = driver.find_element(By.XPATH, '//h1[text() ="no article!"]')
        return {'title':  '', 'url': '', 'content': ''}
    except (NoSuchElementException, WebDriverException) as err:
        logging.warning('Element containing "no article!" not found')
    #detect whether the article is not posted yet
    try:
        title = driver.find_element(By.XPATH, '//body[text() ="not permitted"]')
        return {'title':  '', 'url': '', 'content': ''}
    except (NoSuchElementException, WebDriverException) as err:
        logging.warning('Element containing "not permitted!" not found')

    #detect what article has been posted and its contents
    try:
        title = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/h1[1]').text
        if 'Sale Result' in title:
            coin = get_coin_abbreviation(title)
            main_content = driver.find_element(By.XPATH, f'//span[contains(text(),"We will commence {coin} trading")]')
            content = main_content.text.split('.')
            content = content[0]
            return {'title':  title, 'url': url, 'content': content}

        if 'Gate.io Startup Free Offering:' in title or 'Gate.io Startup:' in title or 'Initial Free Offering:' in title:
            coin = get_coin_abbreviation(title)
            main_content = driver.find_element(By.XPATH, f'//div[@class="dtl-content"]')
            content = main_content.text.split('(2) ')
            content = content[1].split(',')
            content = content[0]
            return {'title':  title, 'url': url, 'content': content}

        if 'Gate.io will list' in title:
            curr_year = str(date.today().year)
            main_content = driver.find_element(By.CLASS_NAME, 'dtl-content')
            content = main_content.text.split(curr_year)
            content = content[0]
            return {'title':  title, 'url': url, 'content': content}
        driver.quit()
        return {'title':  title, 'url': url, 'content': ''}
    except (NoSuchElementException, WebDriverException, Exception) as err:
        logging.warning('No title found', err)
        driver.quit()
        return {'title':  '', 'url': '', 'content': ''}

def get_url(url):
    payload = "tags_query=&title_query=&cate_query=lastest"
    headers = {
        "cookie": "lang=en; curr_fiat=USD; market_title=usdt; defaultBuyCryptoFiat=EUR; _ga=GA1.2.1735262583.1657554676; _uetvid=cbee6840050911ed93dd19846032d0f6; b_notify=1; notify_close=kyc; show_zero_funds=1; chatroom_lang=en; ch=ann27383; idb=1659275456; login_notice_check=^%^2F; _gid=GA1.2.994940262.1659613700; lasturl=^%^2Farticlelist^%^2Fann; _gat_UA-1833997-40=1; _gat_gtag_UA_222583338_1=1; _gat_gtag_UA_1833997_38=1; AWSALB=W2CRJEDp8Bl/QNG502EecWzZRunBNdLU2N6gwGdtXjWxfeg9g9gGEfrhaIVlO3/i+BUrWw7PWKQdO+WUaUfkEuU2uZR29pppmlbuSEczz57WT7bbmmiKNT1PSFiE; AWSALBCORS=W2CRJEDp8Bl/QNG502EecWzZRunBNdLU2N6gwGdtXjWxfeg9g9gGEfrhaIVlO3/i+BUrWw7PWKQdO+WUaUfkEuU2uZR29pppmlbuSEczz57WT7bbmmiKNT1PSFiE",
        "authority": "www.gate.io",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9,hr;q=0.8,bs;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "null",
        "pragma": "no-cache",
        "sec-ch-ua": "^\^.Not/A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"
    }
    try:
        res = requests.request("GET", url, data=payload, headers=headers)
        if res.status_code != 200:
            raise Exception(
            "Gateio scraper encountered an error: {} {}".format(
                res.status_code, res.text
            )
        )
        return res
    except (Exception) as e:
        logging.error(f'Exception occured while fetching gateio url: \n{e}')

def get_article_number(url):
    article_number = url.split('article/')
    article_number = int(article_number[1])
    return article_number

def scrape_article_list(latest_article):
    try:
        url = "https://www.gate.io/articlelist/ann/0"
        response = get_url(url)
        html = BeautifulSoup(response.text, 'html.parser')
        item_list = html.find_all('div', class_='latnewslist')
        new_articles = []
        for i in item_list:
            title = i.find('h3').text
            url = i.find('a').get('href')
            article_number = int(url.split('/article/')[1])
            if article_number > latest_article:
                new_articles.append({'title': title, 'url': url})
        return new_articles
    except (RemoteDisconnected, ConnectionError, ProtocolError, Exception) as e:
        logging.error(f'Exception occured while scraping Gate.io: \n{e}')
        return []

def scrape_article(url):
    try:
        response = get_url(url)
        html = BeautifulSoup(response.content, 'html.parser')
        title = html.find_all('h1')[0].text
        content = html.find('div', class_='dtl-content')
        if response.status_code != 200: return {'title':  '', 'url': '', 'content': ''}
        if title == 'not permitted' or 'no article!' in title or title == '': return {'title':  '', 'url': '', 'content': ''}

        if 'Sale Result' in title:
            coin = get_coin_abbreviation(title).lower()
            content = content.find_all('span')
            for c in content:
                if f'we will commence {coin} trading' in c.text.lower():
                    content = c.text
                    break
            content = content.split('.')
            content = content[0]
            return {'title':  title, 'url': url, 'content': content}

        if 'Gate.io Startup Free Offering:' in title or 'Gate.io Startup:' in title or 'Initial Free Offering:' in title:
            coin = get_coin_abbreviation(title)
            content = content.find_all('br')
            for c in content:
                if f'trading starts' in c.text.lower():
                    content = c.text.lower()
                    break
            content = content.split('trading starts ')
            content = content[1].split(',')
            content = 'Trading starts ' + content[0]
            content += ' UTC'
            return {'title':  title, 'url': url, 'content': content}

        if 'Gate.io will list' in title:
            content = content.find_all('strong')
            content = content[0].text
            return {'title':  title, 'url': url, 'content': content}
    except (AttributeError, requests.exceptions.ConnectionError, Exception) as e:
        article_number = get_article_number(url)
        logging.exception(f'Exception while scraping article {article_number} on gateio: \n{e}')
        return {'title':  '', 'url': '', 'content': ''}

def get_exchanges(title):
    coin = get_gate_coin(title)
    markets_list = get_coin_markets(coin)
    markets = concat_markets(markets_list)
    return markets

def process_article(a):
    title = a['title']
    url = 'https://www.gate.io' + a['url']
    if 'Sale Result' in title or 'Gate.io Startup Free Offering:' in title or 'Gate.io Startup:' in title or 'Initial Free Offering:' in title or 'Gate.io will list' in title:
        article = scrape_article(url)
        try:
            if not article['title'] == '' and article['content'] == '':
                send_gateio_article_alert(article['title'], ['link'])
            else:
                exchanges = get_exchanges(article['title'])
                send_gateio_listing_alert(article, exchanges)
        except requests.exceptions.ConnectionError as err:
            logging.error(f'Error sending an alert: \n{err}')
        
    else:
        send_gateio_article_alert(title, url)
        logging.info('NEW ARTICLE ALERT! Detecting listings in articles...')

def get_latest_article():
    articles = scrape_article_list(0)
    latest_article = get_article_number(articles[0]['url'])
    logging.info(f'Successfully loaded most recent article number: {latest_article}')
    return latest_article
 
def gateio():
    latest_article = get_latest_article()
    while(True):
        new_articles = scrape_article_list(latest_article)
        if len(new_articles) > 0:
            latest_article = get_article_number(new_articles[0]['url'])
        for a in reversed(new_articles):
            process_article(a)
            if len(new_articles) > 1:
                sleep(randint(30, 50))
        timeout = randint(50, 80)
        logging.info(f'Looking for News/Announcements in {timeout} seconds')
        sleep(timeout)

def start_gateio_websocket():
    app = GateWebSocketApp("wss://api.gateio.ws/ws/v4/",
        "BB1A0403-D004-473C-B972-CD1CBC19FFBC",
        "dcaabe74c365de13b411a3abf255d12f54016a76c8a3f5ecc1b895367606df6c",
        on_message=on_message,
        on_open=on_open)
    app.run_forever(ping_interval=5)
