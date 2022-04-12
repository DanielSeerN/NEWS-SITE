from news_show.parsers.cybersports_ru_parser import parse_cybersport_ru_news
from .models import NewsArticle, SourceCategory, Reader

import json


def get_article_by_slug(kwargs):
    article = NewsArticle.objects.get(slug=kwargs.get('slug'))
    return article


def get_reader(request):
    reader = Reader.objects.get(user=request.user)
    return reader


def get_all_news():
    all_news = NewsArticle.objects.all().order_by('post_time')
    return all_news


def get_all_categories():
    all_categories = SourceCategory.objects.all()
    return all_categories


def get_category(kwargs):
    category = SourceCategory.objects.get(slug=kwargs.get('slug'))
    return category


def get_articles_by_category(category):
    articles = NewsArticle.objects.filter(source=category)
    return articles


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
