import requests
import os
import logging

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