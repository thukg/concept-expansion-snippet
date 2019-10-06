import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import urllib
import config

session_google = requests.Session()
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
conn = sqlite3.connect(config.path_list.snippets_en)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS search (name TEXT PRIMARY KEY NOT NULL, page0 TEXT NOT NULL, page1 TEXT NOT NULL, page2 TEXT NOT NULL)')
conn.commit()
conn.close()
tot_crawl = 0

def clean_snippet(text):
    text = re.sub(r'\n|\r', '', text)
    return text

def load_snippet_google(name):
    name = urllib.parse.quote_plus(name)
    snippets = []
    for i in range(0, 3):
        time.sleep(1+random.random())
        url = 'https://www.google.com.hk/search?gws_rd=cr&newwindow=1&start=' + str(i*10) + '&q=' + name
        headers = {'user-agent': USER_AGENT, 'origin': 'https://www.google.com.hk/', 'referer': 'https://www.google.com.hk/', 'x-client-data': 'CKW1yQEIirbJAQiltskBCMS2yQEIqZ3KAQioo8oBCL+nygEI7KfKAQjiqMoBGPmlygE='}
        page = session_google.get(url=url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        snippet = ''
        tmp = soup.find('div', class_='LGOjhe')
        if tmp is not None:
            snippet += clean_snippet(tmp.text) + '\n'
        tmp = soup.find('div', class_='hb8SAc kno-fb-ctx')
        if tmp is not None:
            snippet += clean_snippet(tmp.text) + '\n'
        tmps = soup.find_all('span', class_='st')
        for tmp in tmps:
            snippet += clean_snippet(tmp.text) + '\n'
        snippets.append(snippet)
    return snippets

def get_snippet(concept):
    global tot_crawl
    conn = sqlite3.connect(config.path_list.snippets_en)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM search WHERE name="' + concept + '"')
    res = cursor.fetchall()
    if not res:
        tot_crawl += 1
        if tot_crawl % 10 == 0:
            time.sleep(20)
        while True:
            search = load_snippet_google(concept)
            if search is None:
                print('get snippet timeout:', concept)
                session_google = requests.Session()
                time.sleep(20)
            else:
                break
        print('get search:', concept)
        tmp = 'INSERT INTO search (name, page0, page1, page2) VALUES (?,?,?,?)'
        cursor.execute(tmp, (concept, search[0], search[1], search[2]))
        conn.commit()
    else:
        search = [res[0][1], res[0][2], res[0][3]]
    conn.close()
    res = '\n'.join(search)
    return re.sub('\n|\r', ' ', res)

if __name__ == '__main__':
    res = get_snippet('wikipedia')
    print(res)