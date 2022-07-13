from discord_webhook import DiscordWebhook

def send_listing_alert(title, time, link, markets):
    exchanges = '| '
    for m in markets:
        exchanges += m + ' | '
    webhook_url  =  'https://discord.com/api/webhooks/996078318384320653/3BWf0odCbyl3VGhQ3keLU73L7plpxuoAjkk5pvU43nb4KeZmHZgGgmSguzP7A7aSq-vy'
    content  = f'@everyone\n{title}\n{time}\nAlready listed on: {exchanges}\nLink to article: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_new_article_alert(title, link):
    webhook_url = 'https://discord.com/api/webhooks/996096673296158802/YoCKtBCgzJiVMzJvW6Og481jRM9rClcsPJdmBTz0ZOhL2U3oDnnAqRwfUwleV4MuFREJ'
    content = f'New Article Released on Gate.io: {title}\nLink to article: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()