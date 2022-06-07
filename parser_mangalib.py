# import requests
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import re
from time import sleep


def result_hendler(dict):
    pattern = r'В тайтле'
    new_result = {}
    for url, title in dict.items():
        if url[0] == '/':
            url = 'https://mangalib.me' + url
        new_result[url] = re.sub(pattern, ' В тайтле', title)
    return new_result


def parser_page(browser):
    parser_dict = {}
    page_source = browser.page_source
    soup = BS(page_source)
    chapter_list = soup.select('.notifications__body > .notifications__list > .notification-row')
    if len(chapter_list):
        for el in chapter_list:
            title = el.select('.notification-item__content > .notification-item__body')
            text = ''
            for entry in title:
                text += entry.get_text()
            a_title = el.select_one('a')
            link = a_title.get('href')
            parser_dict[link] = text
    else:
        parser_dict['no_chapter'] = 'нет уведомлений'
    return parser_dict


def script(browser, login, password):
    elem = browser.find_element_by_id('show-login-button')
    elem.click()
    sleep(1)
    elem = browser.find_element_by_name('email')
    elem.click()
    elem.send_keys(login)
    sleep(1)
    elem = browser.find_element_by_name('password')
    elem.click()
    elem.send_keys(password)
    sleep(1)
    elem = (browser.find_element_by_class_name('form__footer')
            .find_element_by_css_selector('button'))
    elem.click()
    sleep(1)
    elem = browser.find_element_by_class_name('fa-bell')
    elem.click()
    sleep(1)
    elem = browser.find_element_by_class_name('notifications__wrapper')
    elems = elem.find_elements_by_class_name('tabs__item ')
    sleep(1)
    elem = elems[1]
    elem.click()
    sleep(1)


def is_update(result, temp):
    return True if temp != result else False


def get_update(result, temp):
    return temp if temp == result else result


def send_message(result, bot, chat):
    message = ''
    for url, title in result.items():
        message += f'{title}\n{url}\n"***************************"\n'
    bot.send_message(chat.id, message)


def parser_mangalib(bot, chat, url, login, password):
    temp = {}
    while True:
        service = Service(executable_path='c:/webdrivers/chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(service=service, chrome_options=options)
        browser.get(url)
        script(browser, login, password)
        parser_item = parser_page(browser)
        browser.quit()
        result = result_hendler(parser_item)
        if is_update(result, temp):
            temp = get_update(result, temp)
            send_message(temp, bot, chat)
        sleep(600)
