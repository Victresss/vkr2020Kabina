from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import os
# from time import sleep


def get_webdriver_file():
    folder = 'driver'
    for f in os.listdir(folder):
        return os.path.join(folder, f)


def get_filename(url):
    filename = url.split("/")[0]
    if filename == "https:" or filename == "http:":
        filename = url.split("/")[2]
    return filename + ".json"


def save_data(filename, data):
    with open(filename, 'w', newline='', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def read_data(filename):
    try:
        with open(filename, "r") as f:
            data = f.read()
        return json.loads(data)
    except OSError as e:
        print("No such file")
        return {}


def wait_for_page_loaded(driver, delay=3):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.title_contains('|'))
        return True
    except TimeoutException:
        print("Loading took too much time!")
        return False


def get_all_links(get_links, driver):
    links = []
    delay = 3  # seconds
    while True:
        sublinks = get_links(str(driver.page_source))
        links += sublinks
        print("links: {}".format(len(links)))
        try:
            element = driver.find_element_by_css_selector(
                '.page-item.active + .page-item')
        except NoSuchElementException:
            break
        element.click()
        try:
            myElem = WebDriverWait(driver, delay).until(EC.title_contains('|'))
        except TimeoutException:
            print("Loading took too much time!")
            break
    return links


def get_data(url, get_links, parse_link, params=None):
    filepath = get_webdriver_file()
    options = Options()
    options.headless = True
    # options.add_argument("--window-size=1920,1200"
    driver = webdriver.Chrome(options=options, executable_path=filepath)
    driver.get(url)
    if not wait_for_page_loaded(driver):
        return {}
    filename = get_filename(url)
    data = read_data(filename)
    while True:
        links = get_links(str(driver.page_source))
        for link in links:
            if link in data.keys():
                continue
            print(link)
            driver.get(link)
            if not wait_for_page_loaded(driver):
                break
            value = parse_link(str(driver.page_source))
            if value != None:
                data[link] = value
                save_data(filename, data)
                print('saved')
            else:
                print("not saved")
            try:
                element = driver.find_element_by_css_selector(
                    '.page-item.active + .page-item')
            except NoSuchElementException:
                break
        element.click()
        if not wait_for_page_loaded(driver):
            break

    return data

    