from news_show.parsers.cybersports_ru_parser import parse_cybersport_ru_news
from .models import NewsArticle, SourceCategory

import json


def create_news_articles(path):
    """
    Создание статьи или проверка её существования
    """

    all_articles = []
    with open(f'{path}', 'r', encoding='utf-8') as file:  # path - путь к файлу с инфой со всех постов
        articles = json.load(file)
        for news_article in articles:
            source = SourceCategory.objects.get(title=news_article['article_source'])
            if NewsArticle.objects.filter(slug=news_article['article_mark']).exists():
                continue
            else:
                news_object = NewsArticle.objects.create(title=news_article['article_title'],
                                                         category=news_article['article_category'],
                                                         news_link=news_article['article_url'],
                                                         post_time=news_article['article_post_time'],
                                                         slug=news_article['article_mark'],
                                                         source=source,
                                                         text=news_article['article_text']
                                                         )
                all_articles.append(news_object)

    return all_articles


def parse_news():
    """
    Функция для регулярного парсинга статей.
    """
    # здесь подключать свои парсеры
    parse_cybersport_ru_news()


def create_news():
    create_news_articles('news_data/cyberspostru_news.json')


def make_news():
    parse_news()
    create_news()


if __name__ == '__main__':
    make_news()
