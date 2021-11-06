
from django.shortcuts import render
from .models import NewsArticle
from .create_news import make_news


def do_main_news(request):
    make_news()
    all_news = NewsArticle.objects.order_by('post_time')
    context = {
        'all_news': all_news
    }
    return render(request, 'news_show/index.html', context)


def get_cybersport_ru_news(request):
    news = NewsArticle.objects.filter(slug='cybersport-ru')
    context = {
        'cybersport_ru_news': news
    }
    return render(request, 'news_show/cybersport_ru.html', context)


def get_cyber_sport_ru_news(request):
    news = NewsArticle.objects.filter(slug='cyber-sport-ru')
    context = {
        'cyber_sport_ru_news': news
    }
    return render(request, 'news_show/cyber_sport_ru.html', context)


# Create your views here.
