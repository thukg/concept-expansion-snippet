import sqlite3
import requests
from bs4 import BeautifulSoup
from hanziconv import HanziConv
import re
import time
import random
import paras
from urllib.parse import quote

session_baidu = requests.Session()
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
conn = sqlite3.connect(paras.path_list.snippets_zh)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS search (name TEXT PRIMARY KEY NOT NULL, page0 TEXT NOT NULL, page1 TEXT NOT NULL, page2 TEXT NOT NULL)')
conn.commit()
conn.close()

def clean_snippet(text):
    text = re.sub(r'\n|\r|\ ', '', text)
    text = HanziConv.toSimplified(text)
    return text

def load_snippet_baidu(name):
    snippets = []
    time.sleep(1)
    for i in range(0, 3):
        url = 'http://www.baidu.com/s?wd=' + quote(name) + '&pn=' + str(i * 10)
        try:
            page = session_baidu.get(url)
        except Exception as e:
            return None
        soup = BeautifulSoup(page.text, 'html.parser')
        tmp = soup.find('div', class_='c-span18 c-span-last')
        snippet = ''
        if tmp is not None:
            tmp = tmp.find('p')
            if tmp is not None:
                snippet += clean_snippet(tmp.text) + '\n'
        tmps = soup.find_all('div', class_='c-abstract')
        for tmp in tmps:
            snippet += clean_snippet(tmp.text) + '\n'
        snippets.append(snippet)
    return snippets

def get_snippet(concept):
    conn = sqlite3.connect(paras.path_list.snippets_zh)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM search WHERE name="' + concept + '"')
    res = cursor.fetchall()
    if not res:
        while True:
            search = load_snippet_baidu(concept)
            if search is None:
                print('get snippet timeout:', concept)
                session_baidu = requests.Session()
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
    res = get_snippet('数据结构')
    print(res)