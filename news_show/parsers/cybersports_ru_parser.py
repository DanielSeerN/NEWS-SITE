import json

import requests
from bs4 import BeautifulSoup

URL = 'https://www.cybersport.ru'


def get_html(url):
    """
    Получаем HTML сайта.
    """
    response = requests.get(url).text
    return response


def make_soup(html):
    """
    Создание объекта BeatifulSoup
    """
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_news():
    """
    Обработка HTML и сохранение нужных данных.
    """
    data_dict = []
    html = get_html(URL)
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('a', class_='link_CocWY')
    urls = []
    for url in articles:
        article_url = url.get('href')
        urls.append(URL + article_url)
    for url in urls:
        article_html = get_html(url)
        article_soup = make_soup(article_html)
        article_title = article_soup.find(class_='headerContentWrap_2xAno').find('h1').text
        article_post_time = article_soup.find(class_='materialPub_wFwM0').text
        article_category = article_soup.find(class_='root_0S2Nc tag_dcScC').text
        article_text_tags = article_soup.find(
            class_='text-content js-mediator-article js-mediator-article root_sK2zH content_5HuK5').contents
        text = ''
        for paragraph in article_text_tags:
            text += paragraph.text
            text += '*'
        hot_news = {
            'article_title': article_title,
            'article_url': url,
            'article_post_time': article_post_time,
            'article_category': article_category,
            'article_source': 'Cybersport.ru',
            'article_mark': url.split('/')[-1],
            'article_text': text,
        }
        data_dict.append(hot_news)

    return data_dict


def write_json(news):
    """
    Запись данных в json.
    """
    with open('news_data/cyberspostru_news.json', 'w', encoding='utf-8') as file:
        json.dump(news, file, indent=4, ensure_ascii=False)


def parse_cybersport_ru_news():
    """
    Функция вызова парсера.
    """
    data = get_news()
    write_json(data)


if __name__ == '__main__':
    parse_cybersport_ru_news()
