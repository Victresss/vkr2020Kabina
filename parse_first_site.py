import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.kvmeter.ru/information/homes_series/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36', 'accept': '*/*'}
BUILDS = []


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def save_file(items):
    with open('builds.json', 'w', newline='', encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False)


def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='r')

    links = []
    for item in items:
        links.append(
            item.find().get('href'),
        )
    return links


def get_content(links):
    for link in links:
        html = get_html(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('table', class_='home_series')

        for item in items:
            BUILDS.append({
                'name': item.find('td', class_='hs_type').get_text(),
                'title': item.find('td').get_text(strip=True),
            })
    return BUILDS


def parse(url):
    html = get_html(url)
    if html.status_code == 200:
        # save_file(get_content(html.text))
        save_file(get_content(get_links(html.text)))
    else:
        print('Error html request')
