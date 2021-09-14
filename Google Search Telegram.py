from bs4 import BeautifulSoup as bs
import requests
import datetime
import time
import json

token = open('token.txt', 'r', encoding='UTF-8').read().strip()
last_date = 0

def get_command(content):
    if content.startswith('.search'):
        return content.replace('.search', '').strip()
    else:
        return None

def query(query):
    r = requests.get(f'https://www.google.com/search?q={query}&start=0')
    items = bs(r.content, 'html5lib').find_all('a')

    return_items = []
    for item in items:
        item = item['href']
        if item.startswith('/url?q=http') and 'accounts.google.com' not in item and 'support.google.com' not in item:
            return_items.append(item.replace('/url?q=', ''))
    if return_items == []:
        return ""
    return return_items

while True:
    try:
        data = requests.get(f'https://api.telegram.org/bot{token}/getUpdates').json()['result']
        data = data[len(data)-1]['message']

        message = data['text'].strip()
        date = data['date']
        chat_id = data['chat']['id']

        if  date != last_date:
            search_query = get_command(message.strip().lower())
            if search_query:
                link_list = query(search_query)
                for text in link_list:
                    requests.post(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
                last_date = date
    except:
        pass
