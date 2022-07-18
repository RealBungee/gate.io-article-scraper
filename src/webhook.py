from discord_webhook import DiscordWebhook

def send_gateio_listing_alert(title, time, link, exchanges):
    webhook_url  =  'https://discord.com/api/webhooks/996078318384320653/3BWf0odCbyl3VGhQ3keLU73L7plpxuoAjkk5pvU43nb4KeZmHZgGgmSguzP7A7aSq-vy'
    content  = f'@everyone\n{title}\n{time}\nListed on: {exchanges}\nLink to article: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_gateio_article_alert(title, link):
    webhook_url = 'https://discord.com/api/webhooks/996096673296158802/YoCKtBCgzJiVMzJvW6Og481jRM9rClcsPJdmBTz0ZOhL2U3oDnnAqRwfUwleV4MuFREJ'
    content = f'New Article Released on Gate.io: {title}\nLink to article: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_mexc_listing_alert(title, url, exchanges):
    webhook_url  =  'https://discord.com/api/webhooks/997948193109180457/cbBoLzixK63soVzxIXFJjK3UIv602COz4LkcJ5Av8WRAlxdwrs6mYgcXeYVAJrjYnq9S'
    content  = f'{title}\n{url}\nListed on: {exchanges}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_mexc_article_alert(title, link):
    webhook_url = 'https://discord.com/api/webhooks/996096673296158802/YoCKtBCgzJiVMzJvW6Og481jRM9rClcsPJdmBTz0ZOhL2U3oDnnAqRwfUwleV4MuFREJ'
    content = f'New Article Released on Gate.io: {title}\nLink to article: {link}'
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