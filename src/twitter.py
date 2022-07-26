import os
import requests
import logging
from socket import error
from threading import Thread
from queue import Queue
from time import sleep
from webhook import send_tweet_alert
from storageMethods import save_twitter_accounts, load_twitter_accounts, load_scrapeData_file

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHYFOQEAAAAAotRfiWhRaZJG2bnG%2BUwv2d7ebho%3Dt6y5qpIBZ7aGcivxrmO1StTpjvR1ozBypmRYbQKxiJ6Vo3VIs8'

def create_url(user_id):
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

def get_params():
    return {"tweet.fields": "created_at", "expansions": "author_id", "user.fields": "name", "exclude": "replies"}

def get_since_params(since_id):
    return {"tweet.fields": "created_at", "expansions": "author_id", "user.fields": "name", "exclude": "replies", "since_id": since_id}

def bearer_oauth(r):
    #bearer_token = os.environ.get("BEARER_TOKEN")
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_tweets(user_id, since='', attempt = 0):
    logging.info(f'Fetching tweets for {user_id}')
    url = create_url(user_id)
    params = get_params()
    if since != '':
        params.update({"since_id": since})
    try:
        json_res = connect_to_endpoint(url, params)
        return json_res
    except (requests.RequestException, requests.ConnectionError, requests.Timeout) as err:
        if type(err) == requests.ConnectionError and attempt < 5:
            attempt += 1
            logging.info(f'Connection was closed, attempting to fetch tweets again. Attempt: {attempt}.')
            get_tweets(user_id, since, attempt)
        else:
            logging.error(f'Error fetching tweets for {user_id}:\n{err}')

def process_information(res, a):
    try:
        user_id = a['user_id']
        username = a['username']
        if res['meta']['result_count'] != 0:
            username = res['includes']['users'][0]['username']
            a['latest_tweet'] = res['meta']['newest_id']
            a['username'] = username
            for t in reversed(res['data']):
                tweet_id = t['id']
                url = 'https://twitter.com/{}/status/{}'.format(username, tweet_id)
                if initialized: send_tweet_alert(username, url)
    except Exception as err:
        logging.info(f'For user: {username} with ID: {user_id} an error occured: {err}')

def process_tweets():
    while True:
        a = q.get()
        res = get_tweets(a['user_id'], a['latest_tweet'])
        process_information(res, a)
        q.task_done()

def twitter():
    logging.info('Starting twitter terminal')
    accounts = load_twitter_accounts()
    global initialized
    initialized = False
    while(True):
        global q 
        q = Queue(len(accounts))
        for a in accounts:
            t = Thread(target=process_tweets)
            t.daemon=True
            t.start()
        try:
            for a in accounts:
                q.put(a)
            q.join()
        except Exception as ex:
            print(ex)
        if not initialized: initialized = True
        #save the most recent tweet information to file
        logging.info('Saving new twitter information')
        save_twitter_accounts(accounts)
        sleep(360)

def get_tweets_from_single_account():
    a = {"user_id": "902839045356744704", "latest_tweet": "1550413482725900288", "username": "justinsuntron"}
    user = a['username']
    user_id = a['user_id']
    try:
        res = get_tweets(a['user_id'])
        print(res)
        if res['meta']['result_count'] != 0:
            username = res['includes']['users'][0]['username']
            a['latest_tweet'] = res['meta']['newest_id']
            a['username'] = username
            for t in res['data']:
                tweet_id = t['id']
                url = 'https://twitter.com/{}/status/{}'.format(username, tweet_id)
                if initialized: send_tweet_alert(username, url)
    except Exception as err:
        print(f'For user: {user} with ID: {user_id} an error occured: {err}')

#used for loading extra information - possibly used only once
def scraped_coin_processing():
    coins = load_scrapeData_file()
    twitter_accounts = []
    for c in coins:
        try:
            for t in c['twitter']:
                twitter_accounts.append({'user_id': t['ID'], 'latest_tweet': '', 'username': t['handle']})
        except KeyError:
            continue
    save_twitter_accounts(twitter_accounts)

#old twitter function
def old():
    accounts = load_twitter_accounts()
    while(True):
        for a in accounts:
            user = a['username']
            id = a['user_id']
            try:
                res = get_tweets(a['user_id'], a['latest_tweet'])
                if res['meta']['result_count'] != 0:
                    username = res['includes']['users'][0]['username']
                    a['latest_tweet'] = res['meta']['newest_id']
                    a['username'] = username
                    for t in res['data']:
                        tweet_id = t['id']
                        url = 'https://twitter.com/{}/status/{}'.format(username, tweet_id)
                        #if initialized: send_tweet_alert(username, url)
            except Exception as err:
                print(f'For user: {user} with ID: {id} an error occured: {err}')
        
        if not initialized: initialized = True
        #save the most recent tweet information to file
        save_twitter_accounts(accounts)
        sleep(360)