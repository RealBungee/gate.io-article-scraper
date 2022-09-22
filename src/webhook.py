from random import randint
from discord_webhook import DiscordWebhook

def send_gateio_listing_alert(article, exchanges):
    title = article['title']
    content = article['content']
    url = article['url']
    webhook_url  =  'https://discord.com/api/webhooks/996078318384320653/3BWf0odCbyl3VGhQ3keLU73L7plpxuoAjkk5pvU43nb4KeZmHZgGgmSguzP7A7aSq-vy'
    content  = f'@everyone\n{title}\n{content}\nListed on: {exchanges}\nLink to article: {url}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_gateio_article_alert(title, link):
    webhook_url = 'https://discord.com/api/webhooks/996096673296158802/YoCKtBCgzJiVMzJvW6Og481jRM9rClcsPJdmBTz0ZOhL2U3oDnnAqRwfUwleV4MuFREJ'
    content = f'{title}\nLink to article: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_mexc_listing_alert(title, url, exchanges):
    webhook_url  =  'https://discord.com/api/webhooks/997948193109180457/cbBoLzixK63soVzxIXFJjK3UIv602COz4LkcJ5Av8WRAlxdwrs6mYgcXeYVAJrjYnq9S'
    content  = f'{title}\n{url}\nListed on: {exchanges}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_mexc_article_alert(title, link):
    webhook_url = 'https://discord.com/api/webhooks/997948280396861550/r-a60qDceofPXpv4Xc98MWbBOWhOkpEePhY61z-1RBjTIzIkFtZGn8vG6ufKAU1BCPow'
    content = f'{title}\nLink to article: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()    

def send_kucoin_listing_alert(title, url, exchanges):
    webhook_url  =  'https://discord.com/api/webhooks/1002851145384984666/1RuFg5C0xmmmYh4EWw7GGvSoUZOkJoRcOUrmwVveCCXBGXzWkUStBt8gq4vNWlta1QOj'
    content  = f'{title}\n{url}\nListed on: {exchanges}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_perp_listing_alert(title, link, token):
    webhook_url = 'https://discord.com/api/webhooks/997498164640743546/4OUHRWpJaqtvpCJLJTvJLc5kIfxquatQlhjwhUZrXeifwwCJr1slqUYq2b-rIwoF-JLK'
    content = f'New Perpetual Listing on {title}: {token}\nLink to listing: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_perp_delisting_alert(title, link, token):
    webhook_url = 'https://discord.com/api/webhooks/997498927286857779/iS0jq0o3stxb5MPsqi6lCQj4qE9nsjY_yT9x9ZZjgsAbYTAvFiFTYAmL2HVgY-USCFx6'
    content = f'New Perpetual Delisting on {title}: {token}\nLink to listing: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_tweet_alert(user, url):
    webhook_url = 'https://discord.com/api/webhooks/999640989780164658/3FcS9JlB1V6srLgExPZnICzpPKt28-bVhGcDIvkaN6x9voVIevIUKQQ5ZODZhDjGRcOd'
    content = f'New tweet from {user}:\n{url}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_gateio_trade_alert(content):
    webhook_url = 'https://discord.com/api/webhooks/1006154058681290783/gfjFp7a5CRaX-aR4Nj-pdecVzoeg4t4aIYH0oiNP3mSzB6dFqMSMoqj-IcjSa1sXblEC'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_mexc_beta_listing_alert(content):
    webhook_url = 'https://discord.com/api/webhooks/1022604008059314246/DBYbQqx0fGmJJPsV0VStzXC5LD2qezZnJZgEPUKNnCUvkjPg67tym57YY40DAS3-9Ypv'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_kucoin_trade_alert(content):
    webhook1_url = 'https://discordapp.com/api/webhooks/1018623147068633309/tUcnjgNFWy5eLDoZEQjsn3rwSQpSS2AGuZBXU5IUxk2PGuRbTsiAzioyt_5Oyxx1tdad'
    webhook2_url = 'https://discord.com/api/webhooks/1008373350873170041/eUfcLGp6O6zd_LqErImXz5hacdcA0KIiGGva4hBaHPxt1vLlyeDvPLoYLBoRUWwpA9rc'
    i = randint(1, 2)
    if i == 1: url = webhook1_url
    else: url = webhook2_url
    webhook = DiscordWebhook(url = url, content = content, rate_limit_retry=False)
    webhook.execute()