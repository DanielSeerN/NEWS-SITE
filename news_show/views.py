import json

from django.shortcuts import render
from django.views import View
from .models import NewsArticle, LatestNews, Category


def get_news(request):
    all_news = []
    with open('news_data/cyberspostru_news.json', 'r', encoding='utf-8') as file:
        cybersport_ru_news = json.load(file)
        for news_article in cybersport_ru_news:
            news_object = NewsArticle()
            news_object.title = news_article['article_title']
            news_object.category = news_article['article_category']
            news_object.news_link = news_article['article_url']
            news_object.post_time = news_article['article_post_time']
            news_object.source = news_article['article_source']
            all_news.append(news_object)
    with open('news_data/cyber_sports_ru.json', 'r', encoding='utf-8') as file1:
        cyber_sport_ru_news = json.load(file1)
        for article in cyber_sport_ru_news:
            article_object = NewsArticle()
            article_object.title = article['article_title']
            article_object.post_time = article['article_post_time']
            article_object.news_link = article['article_url']
            article_object.source = article['article_source']
            all_news.append(article_object)
    context = {
        'all_news': all_news
    }
    return render(request, 'news_show/index.html', context)


def view(request):
    return render(request, 'news_show/index.html')

# Create your views here.
