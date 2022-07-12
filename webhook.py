from discord_webhook import DiscordWebhook

def send_listing_alert(title, time, link):
    webhook_url  =  'url'
    content  = f'@everyone\n{title}\n{time}\nLink to article: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()

def send_new_article_alert(title, link):
    webhook_url = 'url'
    content = f'New Article Released on Gate.io: {title}\nLink to article: {link}'
    webhook = DiscordWebhook(url = webhook_url, content = content, rate_limit_retry=True)
    webhook.execute()