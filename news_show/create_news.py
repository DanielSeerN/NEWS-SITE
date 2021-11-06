from .utils import create_news_articles
import time
from .models import NewsArticle
from .cybersports_ru_parser import parse_cybersport_ru_news
from .cyber_sports_parser import parse_cyber_sport_ru_news


def create_news():
    NewsArticle.objects.all().delete()
    parse_cybersport_ru_news()
    parse_cyber_sport_ru_news()
    cybersport_ru_news = create_news_articles('news_data/cyberspostru_news.json')
    cyber_sport_ru_news = create_news_articles('news_data/cyber_sports_ru.json')


def make_news():
    create_news()


if __name__ == '__main__':
    make_news()
