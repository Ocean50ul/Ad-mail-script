from bs4 import BeautifulSoup as bs
import requests as rq
import sqlite3 as sq
import time
from random import randint
from secret import path

URL = 'https://realty.yandex.ru/moskva/kupit/kommercheskaya-nedvizhimost/?commercialType=OFFICE&commercialType=FREE_PURPOSE&priceMax=100000&priceMin=0&priceType=PER_METER&commercialBuildingType=DETACHED_BUILDING&areaMin=1500'
HEADERS = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def sleep_countdown():
    time_to_sleep = randint(8, 13)
    for i in range(1, time_to_sleep + 1):
        print(f'Stupid yandex wont let me parse until i count {i}/{time_to_sleep}', end='\r')
        time.sleep(1)
    print('\n')



def number_of_pages():
    '''Returns number of pages from URL'''
    number = randint(20, 50)
    url = f'https://realty.yandex.ru/moskva/kupit/kommercheskaya-nedvizhimost/?commercialType=OFFICE&commercialType=FREE_PURPOSE&priceMax=100000&priceMin=0&priceType=PER_METER&commercialBuildingType=DETACHED_BUILDING&areaMin=1500&page={number}'
    get_response = rq.get(url, headers=HEADERS)
    soup = bs(get_response.content, 'lxml')
    all_pages = [int(page.text) for page in soup.find_all('a', class_='Pager__radio-link') if 1 <= len(page.text) <= 2]
    print('Number of pages is extracted!')
    return max(all_pages)


def page_injector(url, page):
    ans = url + f'&page={page}'
    return ans


def links_extractor(url):
    ans = []
    get_response = rq.get(url, headers=HEADERS)
    soup = bs(get_response.content, 'lxml')
    links = [link.get('href') for link in soup.find_all('a', class_='Link')]
    for link in links:
        if link.startswith('/offer/'):
            link = 'https://realty.yandex.ru/' + link
            if link not in ans:
                ans.append(link)
    return ans


def all_links_from_all_pages():
    ans = []
    pages = number_of_pages()
    sleep_countdown()
    for page in range(pages):
        url = page_injector(URL, page)
        links = links_extractor(url)
        ans.extend(links)
        if page != (pages - 1):
            sleep_countdown()
    return ans


#def address_exctractor():
    #'''Extracts address from url if soup object is predefined (to avoid too many get responses) (to avoid all duplicates in future) (+ db upadate should be implemented) (not tested yet)'''
   #addresses = [adress.text for adress in soup.find_all('div', class_='cozPT08Lv7Nk5AQItem__address')]
   #return addresses


def db_check(item):
    '''True or false'''
    connection = sq.connect(path)
    cursor = connection.cursor()
    cursor.execute('SELECT Link FROM Links WHERE Link = (?)', (item,))
    data = cursor.fetchall()

    if data == []:
        cursor.close()
        return False
    cursor.close()
    return True


def db_insert(item):
    connection = sq.connect(path)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Links (Link) VALUES (?)', (item,))
    connection.commit()
    cursor.close()


def mail_list():
    ans = []
    for link in all_links_from_all_pages():
        if not db_check(link):
            ans.append(link)
            db_insert(link)
        else:
            continue
    if ans == []:
        ans = ['Сегодня ничего нет!']
    print('Synchronyzed with db!')
    return ans