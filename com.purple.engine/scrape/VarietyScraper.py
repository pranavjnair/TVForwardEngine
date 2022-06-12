import datetime

from bs4 import BeautifulSoup
import requests
import pandas as pd

session = requests.Session()

session.headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }
)

page_number = 1
base_url = 'https://variety.com/v/tv/'
page_url = 'https://variety.com/v/tv/page/' + str(page_number) + '/'
page_limit = 10

try:
    news_list = []
    for i in range(page_number, page_limit + 1):
        if i == 1:
            session_url = base_url
        else:
            session_url = base_url + 'page/' + str(i) + '/'
        web_page = session.get(session_url)
        soup = BeautifulSoup(web_page.text, "html.parser")
        web_page_attrs = soup.find_all('li', attrs={'class': 'o-tease-list__item'})

        news_sub_list = []
        for attr in web_page_attrs:
            title = attr.find("h3", attrs={'id': 'title-of-a-story'})
            if title is None:
                break
            else:
                title = title.find('a').text.strip()
            link = attr.find("h3", attrs={'id': 'title-of-a-story'})
            if link is None:
                break
            else:
                link = link.find('a')['href']
            date = datetime.date.today().strftime("%Y-%m-%d")

            news_list.append([title, link, date])

    variety_data = pd.DataFrame(news_list, columns=['Title', 'Link', 'Date'])
    # print(variety_data)

except Exception as e:
    print(e.__str__())
