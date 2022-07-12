import csv
import logging
from time import sleep
from scraper import check_for_article
from webhook import send_new_article_alert, send_listing_alert

def save_latest_article(article_number):
    myFile = open('latest_article.csv', 'w', newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(article_number)

def load_latest_article():
    article_num = ''
    with open('latest_article.csv', newline='') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            article_num = row
    return article_num[0]

def main():
    article_number = int(load_latest_article())
    while(True):
        title, link, content = check_for_article(article_number)
        if not("no article!" in title):
            if content != '':
                send_listing_alert(title, content, link)
            else:
                send_new_article_alert(title, link)
            article_number += 1
            save_latest_article([article_number])
        logging.info('Article not found - checking again in 60 seconds')
        sleep(60)
main()