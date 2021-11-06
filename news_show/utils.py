import json
from .models import NewsArticle


def create_news_articles(path):
    all_articles = []
    with open(f'{path}', 'r', encoding='utf-8') as file:
        articles = json.load(file)
        for news_article in articles:
            news_object = NewsArticle()
            news_object.title = news_article['article_title']
            news_object.category = news_article['article_category']
            news_object.news_link = news_article['article_url']
            news_object.post_time = news_article['article_post_time']
            news_object.slug = news_article['article_source']
            all_articles.append(news_object)
            news_object.save()
    return all_articles
