import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

# para rodar o chrome em 2º plano
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.headless = True
# navegador = webdriver.Chrome(options=chrome_options)


# abrir um navegador
ser = Service("C:/Users/Leonny Sousa/PycharmProjects/Web_Scraping_Mercado_Livre/chromedriver.exe")
op = webdriver.ChromeOptions()
Web = webdriver.Chrome(service=ser, options=op)


def open_link(url_link):
    Web.get(url_link)
    time.sleep(3)


def scrap_response_and_html(url_link):
    response = requests.get(url_link)
    time.sleep(1)
    site = BeautifulSoup(response.text, 'html.parser')
    time.sleep(3)
    return response, site


def next_page_html():
    nxt = site.find('li', attrs={'class': 'andes-pagination__button andes-pagination__button--next'})
    next_page = nxt.find('a', attrs={'class': 'andes-pagination__link ui-search-link'})['href']
    return next_page


def scrap_products(products):
    list_of_products = []
    for product in products:
        nome = product.find('h2', attrs={'class': "ui-search-item__title"})
        link = product.find('a', attrs={'class': 'ui-search-item__group__element ui-search-link'})

        real = product.find('span', attrs={'class': 'price-tag-fraction'})
        cents = product.find('span', attrs={'class': 'price-tag-cents'})

        if real and cents:
            price = real.text + ',' + cents.text
        else:
            price = real.text

        list_of_products.append([nome.text, price, link['href']])

    return list_of_products


page = 'https://carros.tucarro.com.co/'
count = 1
List = []
writer = pd.ExcelWriter('Produtos.xlsx', engine='xlsxwriter')

while page:
    open_link(page)
    response, site = scrap_response_and_html(page)
    products = site.findAll('div', attrs={
        'class': 'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default'})

    list_of_products = scrap_products(products)
    List = pd.DataFrame(list_of_products, columns=['Title', 'Price', 'Link'])
    List.to_excel(writer, sheet_name='Sheet ' + str(count), index=False)

    try:
        page = next_page_html()
    except:
        print('Não há proxima pagina!!')
        break

    # path = r"C:\Users\Leonny Sousa\PycharmProjects\Produtos.xlsx"

    print(List)
    count = count + 1

writer.save()
