
from django.shortcuts import render
from .models import NewsArticle, FavouriteArticle
from .create_news import make_news


def do_main_news(request):
    make_news()
    all_news = NewsArticle.objects.order_by('post_time')
    context = {
        'all_news': all_news
    }
    return render(request, 'news_show/index.html', context)


def get_cybersport_ru_news(request):
    news = NewsArticle.objects.filter(source='cybersport-ru')
    context = {
        'cybersport_ru_news': news
    }
    return render(request, 'news_show/cybersport_ru.html', context)


def get_cyber_sport_ru_news(request):
    news = NewsArticle.objects.filter(source='cyber-sport-ru')
    context = {
        'cyber_sport_ru_news': news
    }
    return render(request, 'news_show/cyber_sport_ru.html', context)

# def add_favourite_article(request, **kwargs):
#     article_slug = kwargs.get('slug')
#     article = NewsArticle.objects.get(slug=article_slug)
#     favourite_article, created = FavouriteArticle.objects.get_or_create(article=article)
# Create your views here.
