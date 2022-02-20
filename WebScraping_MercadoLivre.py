# Warning: This code is use to Scrap data from the site: "Mercado Livre"
# 1 - Execute this code
# 2 - Type a product name
# 3 - This automatic program will search and Scrape all the products found in the site
# 4 - The results found will be save in a Excel file

# Fist of all, you need to install the libraries: requests, bs4, pandas, selenium, XlsxWriter
# You can find the installation accessing the Links below:

#    - https://pypi.org/project/requests/
#      Requests allows you to send HTTP/1.1 requests extremely easily

#    - https://pypi.org/project/bs4/
#      Beautiful Soup is a Python library for pulling data out of HTML and XML files.

#    - https://pypi.org/project/selenium/
#      Selenium is a powerful tool for controlling web browsers

#    - https://pypi.org/project/pandas/
#      Pandas is a Python package that provides fast, flexible, and expressive data structures
#      designed to make working with "relational" or "labeled" data

#    - https://pypi.org/project/XlsxWriter/
#      Python module for writing files in the Excel


# Import of packages:
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


def open_link(url_link):
    """ This function receives a Url Link and open on the Chrome """
    Web.get(url_link)
    time.sleep(2)


def scrape_response_and_html(url_link):
    """
    This Function is used to get the response HTTP and HTML from an URL LINK
    response = HTTP response
    Site = HTML code
    """
    response = requests.get(url_link)
    time.sleep(1)
    site = BeautifulSoup(response.text, 'html.parser')
    time.sleep(1)
    return response, site


def next_page_html(site):
    """ This function is used to find the Next page URL Link """
    nxt = site.find('li', attrs={'class': 'andes-pagination__button andes-pagination__button--next'})
    next_page = nxt.find('a', attrs={'class': 'andes-pagination__link ui-search-link'})['href']
    return next_page


def current_and_last_page(site):
    """ This function is use to get the current and the last page from the results found """
    try:
        last_page = site.find('li', attrs={'class': "andes-pagination__page-count"})
        current_page = site.find('li', attrs={'class': "andes-pagination__button andes-pagination__button--current"})
        last_page = int(last_page.text[2:])
        current_page = int(current_page.text)
    except (AttributeError, TypeError):
        print("Only 1 Page found!!")
        current_page = 1
        last_page = 1
    return current_page, last_page


def scrape_products(site):
    """
    This function receives the HTML and search for Tags with product information:
    name  =  product name
    Price = Product value
    link = Link where the product can be found
    """
    list_of_products = []
    products = site.findAll('div', attrs={
        'class': 'andes-card andes-card--flat andes-card--default ui-search-result '
                 'ui-search-result--core andes-card--padding-default'})

    for product in products:
        nome = product.find('h2', attrs={'class': "ui-search-item__title"})
        link = product.find('a', attrs={'class': 'ui-search-item__group__element ui-search-link'})

        real = product.find('span', attrs={'class': 'price-tag-fraction'})
        cents = product.find('span', attrs={'class': 'price-tag-cents'})

        if real and cents:
            price = real.text + '.' + cents.text
        else:
            price = real.text

        list_of_products.append([nome.text, price, link['href']])

    return list_of_products


# Link to search a product:
URL_main = 'https://lista.mercadolivre.com.br/'
search_product = input('Type the product you want to search for:')
page = URL_main + search_product

# Opening the Chrome:
ser = Service("C:/Users/Leonny Sousa/PycharmProjects/Web_Scraping_Mercado_Livre/chromedriver.exe")
op = webdriver.ChromeOptions()
Web = webdriver.Chrome(service=ser, options=op)

# Initializating variables
List = []  # list of products on a page
current_page = 0 # Current searching page
last_page = 0 # Last found page

# Opening Excel Writer:
with pd.ExcelWriter('Products.xlsx', engine='xlsxwriter') as writer:
    while current_page <= last_page:
        open_link(page)
        response, site = scrape_response_and_html(page)
        list_of_products = scrape_products(site)
        List = pd.DataFrame(list_of_products, columns=['Title', 'Price', 'Link'])
        current_page, last_page = current_and_last_page(site)


        List.to_excel(writer, sheet_name='Sheet ' + str(current_page), index=False)

        print(List)
        print(f"{current_page} of {last_page} pages")

        if current_page < last_page:
            page = next_page_html(site)
        else:
            break


    
