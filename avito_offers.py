from bs4 import BeautifulSoup as bs
import requests as rq
import time
import sqlite3 as sq
from secret import path

TIME_TO_SLEEP = 10
initial_url = 'https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?pmax=100000&q=%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5&f=ASgBAQECAkSwCNJW8hKi2gEBQIYJJI5dil0CRfoSGXsiZnJvbSI6bnVsbCwidG8iOjEwMDAwMH20Exd7ImZyb20iOjEwMDAsInRvIjpudWxsfQ&i=1&p=1'
get_response = rq.get(initial_url)
soup = bs(get_response.content, 'lxml')
time.sleep(TIME_TO_SLEEP)


def number_of_pages():
    '''Определяет количество страниц в поисковом запросе'''
    ans = 1
    page_objects = soup.find_all(
        'span', class_="pagination-item-1WyVp")
    for i in page_objects:
        try:
            if int(i.text) > ans:
                ans = int(i.text)
        except (ValueError, TypeError):
            continue
    return ans


def page_injector(url, page_number):
    '''Вставляет в ссылку (url) номер страницы (page_number)'''
    url = url[:len(url) - 1]
    url = url + str(page_number)
    return url


def links_exctractor(url):
    '''Извлекает ссылки на объявления из url'''
    print('Extracting links from page..')
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    get_response = rq.get(url, headers=headers)
    soup = bs(get_response.content, 'lxml')
    ans = []
    a_class = soup.find_all('a', class_='snippet-link')
    for item in a_class:
        href = item.get('href')
        if not href.startswith('/moskva'):
            continue
        proper_link = 'https://www.avito.ru' + href
        ans.append(proper_link)
    return ans


def all_links_all_pages():
    '''Список из всех ссылок со всех страниц'''
    ans = []
    for page_number in range(1, number_of_pages() + 1):
        print(f'Page is {page_number}/{number_of_pages()}..')
        url = page_injector(initial_url, page_number)
        ans = ans + links_exctractor(url)
        time.sleep(TIME_TO_SLEEP)
    return ans


def address_exctractor():
    '''Returns list of addresses (corresponded with links list) if soup object of a page is predefined'''
    ans = []
    addresses = soup.find_all('span', class_='item-address__string')
    for address in addresses:
        ans.append(address.text.strip())
    return ans


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


def links_to_mail():
    '''Сверяется с дб и делает окончательный список ссылок на отпарвку'''
    ans = []
    for link in all_links_all_pages():
        if not db_check(link):
            ans.append(link)
            db_insert(link)
        else:
            continue
    if ans == []:
        ans = ['Сегодня ничего нет!']
    print('Synchronized with db!')
    return ans
