import requests
from bs4 import BeautifulSoup

# url = "https://oz.by/books/bestsellers"

def get_html(url):
    response = requests.get(url)
    return response.text

def get_max_number_page(html):
    max_number = 1
    soup = BeautifulSoup(html, 'lxml')
    li = soup.find('ul', class_="g-pagination__list").find_all('li', class_="pg-last")

    for a in li:
        max_number = a.find('a', class_="g-pagination__list__item").text

    return max_number

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('ul', id='goods-table').find_all('li', class_='viewer-type-card__li ')
    return links

def get_book_name(link):
    return link.find('p', class_="item-type-card__title").text

def get_author_name(link):
    return link.find('p', class_="item-type-card__info").text
