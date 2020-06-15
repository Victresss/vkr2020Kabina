from scrapper import get_data
from bs4 import BeautifulSoup


def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('table').find_all('a')
    links = []
    for item in items:
      link = item.get('href')
      if not link == "#" and not link.startswith("?"):
        links.append('https://www.reformagkh.ru'+link)
    print(len(links))
    return links


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find(id='list-home').find_all('tr')
    data = {}
    prefix = ""
    for item in items:
        tds = item.find_all('td')
        if 'sub-tr' in item['class']:
            name = prefix + tds[0].text
        elif 'border-bottom-grey' not in item['class']:
            prefix = tds[0].text + ": "
            name = ""
        else:
            prefix = ""
            name = tds[0].text

        if len(name) > 0:
            data[name] = tds[1].text

    print(data)
    return data

def load_data():
    url = 'https://www.reformagkh.ru/myhouse?tid=2227388&limit=60'
    data = get_data(url, get_links, get_content)

    return data
