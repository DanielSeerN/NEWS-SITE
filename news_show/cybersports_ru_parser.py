import json

import requests
from bs4 import BeautifulSoup

URL = 'https://www.cybersport.ru'


def get_html(url):
    response = requests.get(url).text
    return response


def get_news(html):
    data_dict = []
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('div', class_="cs-col-lg-6 cs-col-md-6 cs-col-xs-12 margin-bottom--20")
    for up_article in news:
        article_title = up_article.find('h3',
                                        class_='margin-bottom--0 margin-top--10 fz--22 card-vertical__title').find(
            'a').text
        article_url = URL + up_article.find('a',
                                            class_='responsive-object responsive-object--16by9 animation--image-opacity-90').get(
            'href')
        article_post_time = up_article.find('div',
                                            class_='margin-left--20 margin-right--20 padding-bottom--20 flex-box justify-content--space-between align-items--stretch post-info').find(
            'time').text
        article_category = up_article.find('a', class_='tag').text
        hot_news = {
            'article_title': article_title,
            'article_url': article_url,
            'article_post_time': article_post_time,
            'article_category': article_category,
            'article_source': 'cybersport-ru',
            'article_mark': article_url.split('/')[-1]
        }
        data_dict.append(hot_news)
    write_json(data_dict)


def write_json(news):
    with open('news_data/cyberspostru_news.json', 'w', encoding='utf-8') as file:
        json.dump(news, file, indent=4, ensure_ascii=False)

def parse_cybersport_ru_news():
    get_news(get_html(URL))

if __name__ == '__main__':
    parse_cybersport_ru_news()


