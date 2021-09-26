import json

from django.shortcuts import render
from django.views import View
from .models import NewsArticle, LatestNews, Category



def get_news(request, *args, **kwargs):
        with open('news_files/cyberspostru_news.json', 'r', encoding='utf-8') as file:
            cybersport_ru_news = json.load(file)
            all_news = []
            for news_article in cybersport_ru_news:
                news_object = NewsArticle()
                news_object.title = news_article['article_title']
                news_object.category = news_article['article_category']
                news_object.news_link = news_article['article_url']
                news_object.post_time = news_article['article_post_time']
                all_news.append(news_object)
            context = {
                'all_news': all_news
            }
            return render(request, 'news_show/index.html', context)


def view(request):
    return render(request, 'news_show/index.html')

# Create your views here.
