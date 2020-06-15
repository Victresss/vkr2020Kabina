from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import os
from random import randrange

def get_webdriver_file():
    folder = 'driver'
    for f in os.listdir(folder):
        return os.path.join(folder, f)


def wait_for_page_loaded(driver, delay=3):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.title_contains('|'))
        return True
    except TimeoutException:
        print("Loading took too much time!")
        return False


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find(id='list-home').find_all('tr')
    data = {}
    prefix = ""
    price = 0.125
    floors = 0
    for item in items:
        tds = item.find_all('td')
        if 'sub-tr' in item['class']:
            name = prefix + tds[0].text
        elif 'border-bottom-grey' not in item['class']:
            prefix = tds[0].text + " "
            name = ""
        else:
            prefix = ""
            name = tds[0].text
        if len(name) > 0:
            if name == 'Количество этажей: наибольшее, ед.':
                floors += int(tds[1].text.strip())
            if name == 'Количество этажей: наименьшее, ед.':
                floors += int(tds[1].text.strip())
            if name == 'Количество помещений, в том числе: жилых, ед.':
                price *= int(tds[1].text.strip())
            data[name] = tds[1].text
    price *= floors
    c1 = randrange(1100, 3000, 10)
    c2 = randrange(2100, 4500, 10)
    c3 = randrange(2500, 5500, 10)
    c4 = randrange(3500, 7000, 10)
    c = c1 + c2 + c3 + c4
    price *= c
    data["Цена"] = str(int(price*1000)) + ' р'
    # print(data)
    return data


def get_results(query):
    options = Options()
    options.headless = True
    # options.add_argument("--window-size=1920,1200"
    driver = webdriver.Chrome(
        options=options, executable_path=get_webdriver_file())
    url = 'https://www.reformagkh.ru/search/houses?query=Волгоград%2C+{}'.format(
        query.replace(" ", "+").replace(",", "%2C"))
    print(url)
    driver.get(url)
    if not wait_for_page_loaded(driver):
        return "Ошибка загрузки"
    try:
      driver.find_element_by_css_selector('tbody td:nth-child(1) > a').click()
    except NoSuchElementException:
        return "Не удается найти"
    if not wait_for_page_loaded(driver):
        return "Ошибка загрузки"
    data = get_content(driver.page_source)
    
    return data
