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


def get_news(html):
    """
    Обработка HTML и сохранение нужных данных.
    """
    data_dict = []
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('article')
    for up_article in news:
        article_url = URL + up_article.find('a').get('href')
        article_html = requests.get(article_url).text
        article_soup = BeautifulSoup(article_html, 'lxml')
        article_title = article_soup.find(class_='headerContentWrap_2xAno').find('h1').text
        article_post_time = article_soup.find(class_='materialPub_wFwM0').text
        article_category = article_soup.find(class_='toolsLeft_OZyse').find('a').text
        article_paragraphs = article_soup.find(class_='text-content js-mediator-article js-mediator-article root_sK2zH content_5HuK5').find_all('p')
        article_text = []
        for paragraph in article_paragraphs:
            paragraph = paragraph.text
            article_text.append(paragraph)
        article_text = '*'.join(article_text)  # Соединяем параграфы через звезду, чтобы потом их легко было разделить.
        hot_news = {
            'article_title': article_title,
            'article_url': article_url,
            'article_post_time': article_post_time,
            'article_category': article_category,
            'article_source': 'Cybersport.ru',
            'article_mark': article_url.split('/')[-1],
            'article_text': article_text,
        }
        data_dict.append(hot_news)
    write_json(data_dict)


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
    get_news(get_html(URL))


if __name__ == '__main__':
    parse_cybersport_ru_news()
