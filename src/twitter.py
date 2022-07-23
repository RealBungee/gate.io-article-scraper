import os
import requests
import logging
from time import sleep
from storageMethods import save_twitter_accounts

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

#bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHYFOQEAAAAAotRfiWhRaZJG2bnG%2BUwv2d7ebho%3Dt6y5qpIBZ7aGcivxrmO1StTpjvR1ozBypmRYbQKxiJ6Vo3VIs8'

def create_url(user_id):
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

def get_params():
    return {"tweet.fields": "created_at", "expansions": "author_id", "user.fields": "name", "exclude": "replies"}

def get_since_params(since_id):
    return {"tweet.fields": "created_at", "expansions": "author_id", "user.fields": "name", "exclude": "replies", "since_id": since_id}

def bearer_oauth(r):
    bearer_token = os.environ.get("BEARER_TOKEN")
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
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

def get_tweets(user_id, since=''):
    logging.info(f'Fetching tweets for {user_id}')
    url = create_url(user_id)
    params = get_params()
    #params = get_since_params(since) if since != '' else get_params()
    if since != '':
        params.update({"since_id": since})
    try:
        json_res = connect_to_endpoint(url, params)
        return json_res
    except (requests.RequestException, requests.ConnectionError, requests.Timeout) as err:
        logging.error(f'Error fetching tweets for {user_id}:\n{err}')

def twitter():
    logging.info('Starting twitter terminal')
    # load information into an array or a map
    [1289071298556170240, 1256716686]
    accounts = [{'user_id': 1304552437487939585, 'latest_tweet': 1550003741197221888}, {'user_id':1289071298556170240, 'latest_tweet': 1525110032895025154}]
    initialized = False
    while(True):
        for a in accounts:
            res = get_tweets(a['user_id'], a['latest_tweet'])
            if res['meta']['result_count'] != 0:
                username = res['includes']['users'][0]['username']
                for t in res['data']:
                    tweet_id = t['id']
                    url = 'https://twitter.com/{}/status/{}'.format(username, tweet_id)
                    #if initialized: send_tweet_alert(username, url)
                a['latest_tweet'] = res['meta']['newest_id']
        if not initialized: initialized = True
        #save the most recent tweet information to file
        save_twitter_accounts(accounts)
        sleep(10)