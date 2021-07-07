from bs4 import BeautifulSoup as bs
import requests as rq
import sqlite3 as sq
import time
from random import randint
from secret import path

INITIAL_URL = "https://www.cian.ru/cat.php?building_type_b%5B0%5D=6&building_type_b%5B1%5D=14&building_type_b%5B2%5D=40&currency=2&deal_type=sale&engine_version=2&m2=1&maxprice=100000&minarea=1000&offer_type=offices&office_type%5B0%5D=11&region=1&sort=price_object_order"


def sleep_countdown():
    time_to_sleep = randint(8, 13)
    for i in range(1, time_to_sleep + 1):
        print(f'Stupid cian wont let me parse until i count {i}/{time_to_sleep}', end='\r')
        time.sleep(1)
    print('\n')


def number_of_pages():
    '''Return number of pages in specific url'''
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    get_resnopse = rq.get(INITIAL_URL, headers=headers)
    soup = bs(get_resnopse.content, 'lxml')
    all_pages = soup.find_all('li', class_='_93444fe79c--list-item--2KxXr')
    ans = 1
    for page in all_pages:
        number = int(page.text)
        if number > ans:
            ans = number
    print('Pages number is extracted!')
    sleep_countdown()
    return ans


def page_injector(url, page_number):
    '''Injects into link (url) page number (page_number)'''
    ans = url + f'&p={page_number}'
    return ans


def links_extractor(url):
    '''Returns list of all ad links from page'''
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    get_response = rq.get(url, headers=headers)
    soup = bs(get_response.content, 'lxml')
    ans = []

    ans = [item.get('href') for item in soup.find_all('a', class_='c6e8ba5398--header-link--3XZlV')]
    return ans


def all_links_from_all_pages():
    '''Returns list of all ad links from all possible pages'''
    pages = number_of_pages()
    ans = []
    for page in range(1, pages + 1):
        url = page_injector(INITIAL_URL, page)
        links = links_extractor(url)
        ans.extend(links)
        print(f'Extracting links from {page}/{pages}')
        if page != pages:
            sleep_countdown()
    return ans


#def address_exctractor():
    #'''Returns list of addresses form a page, that is corresponidng with links list'''
    #ans = [address.contents[0].get('content').strip() for address in soup.find_all('div', class_='c6e8ba5398--address-path--2Y559')]
    #return ans


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
    '''Synchronyzing with db so actual mail list could contain only new ads'''
    ans = []
    for link in all_links_from_all_pages():
        if not db_check(link):
            ans.append(link)
            db_insert(link)
        else:
            continue
    if ans == []:
        ans = ['Сегодня ничего нет!']
    print('Synchronized with db!')
    return ans