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
    news = soup.find_all('div', class_="cs-col-lg-6 cs-col-md-6 cs-col-xs-12 margin-bottom--20")
    for up_article in news:
        article_url = up_article.find('a',
                                      class_='inverse-color--black-00').get(
            'href')
        if article_url.split('/')[2] == 'match':
            continue
        if article_url.split('/')[2] != 'www.cybersport.ru':
            article_url = URL + article_url
        article_title = up_article.find('h3',
                                        class_='margin-bottom--0 margin-top--10 fz--22 card-vertical__title').find(
            'a').text

        article_category = up_article.find('a', class_='tag').text
        response = requests.get(article_url).text
        soup = BeautifulSoup(response, 'lxml')
        article_paragraphs = soup.find('section', class_='article__inner').find_all('p')
        article_post_time = soup.find('time', itemprop='datePublished').text
        article_text = []
        for paragraph in article_paragraphs:
            paragraph_text = paragraph.text
            article_text.append(paragraph_text)
        article_text = '*'.join(article_text)  # Соединяем текст через звезду, чтобы потом легко было его разделить.
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
