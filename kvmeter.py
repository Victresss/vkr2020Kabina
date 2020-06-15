from scrapper import get_data
from bs4 import BeautifulSoup


def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='r')
    links = []
    for item in items:
        links.append(
            item.find().get('href'),
        )
    return links


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='home_series')
    try:
        items = list(filter(lambda x: str(x) != '[]', table.find_all('tr')))
    except AttributeError:
        return None
    data = []

    for item in items:
        values = []
        for td in item.find_all('td'):
            if td.has_attr('class'):
                key = td.text.strip()[0:-1]
            else:
                value = td.text.strip()
                if len(value) > 0:
                    values.append(value)
        if len(values) > 0:
            data.append({'key': key, 'values': values})
    return data


def load_data():
    url = 'https://www.kvmeter.ru/information/homes_series/'
    raw_data = get_data(url, get_links, get_content)
    data = {}
    for key in raw_data:
        values = raw_data[key]
        for value in values:
            if value['key'] == 'Регионы строительства':
                if value['values'][0].find("Волгоград") > -1:
                    data[key] = values
                break
    return data
