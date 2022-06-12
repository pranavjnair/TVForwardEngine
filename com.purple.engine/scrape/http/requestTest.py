import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd

session = requests.Session()

session.headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }
)

url = 'https://variety.com/v/tv/'

try:
    web_page = session.get(url)
    # print(web_page.status_code)

    soup = BeautifulSoup(web_page.text, "html.parser")
    # print(soup)

    attrs = {'class': 'o-tease-list__item'}
    web_page_attrs = soup.find_all('li', attrs)
    # print(web_page_attrs)
    # print(len(links))

    print()
    for attr in web_page_attrs:
        # print(attr)
        # title = attr.find('a')['class'].strip()
        attrs = {'id': 'title-of-a-story'}
        text = attr.find("h3", attrs).find('a').text.strip()
        link = attr.find("h3", attrs).find('a')['href']
        print(text)
        print(link)
        print()
        # break
    # print(web_page_attrs.__getitem__(0))
    # print(web_page_attrs.__getitem__(0).text.strip())
    # web_page_attrs_0_stripped = web_page_attrs.__getitem__(0).text.strip()

    # attrs = {'class': 'c-title__link'}
    # web_page_attrs = soup.find_all('li', attrs)

except Exception as e:
    print(e.__str__())
