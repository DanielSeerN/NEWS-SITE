import json

import requests
from bs4 import BeautifulSoup

URL = 'https://cyber.sports.ru/'


def get_html(url):
    response = requests.get(url).text
    return response


def get_news(html):
    data_dict = []
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('article',
                         class_='js-active js-material-list__blogpost material-list__item clearfix piwikTrackContent '
                                'piwikContentIgnoreInteraction')
    for article in news:
        article_title = article.find('a', class_='h2').text
        article_url = article.find('a',
                                   class_='material-list__item-news_show-link material-list__item-news_show-link_float_right').get(
            'href')
        article_post_time = article.find(class_='time-block time-block_top').text
        article_paragraph = article.find('p').text
        request_for_article = requests.get(article_url).text
        article_soup = BeautifulSoup(request_for_article, 'lxml')
        article_text = article_soup.find_all('p', class_='is-regular')


        article_dict = {
            'article_title': article_title,
            'article_url': article_url,
            'article_post_time': article_post_time,
            'article_source': 'cyber-sports-ru',
            'article_category': article_paragraph[:-5],
            'article_mark': article_url.split('/')[-1],
            'article_text': ' '.join(article_text)
        }
        data_dict.append(article_dict)
    write_json(data_dict)


def write_json(data_dict):
    with open('news_data/cyber_sports_ru.json', 'w', encoding='utf-8') as file:
        json.dump(data_dict, file, indent=4, ensure_ascii=False)


def parse_cyber_sport_ru_news():
    get_news(get_html(URL))


if __name__ == '__main__':
    parse_cyber_sport_ru_news()
