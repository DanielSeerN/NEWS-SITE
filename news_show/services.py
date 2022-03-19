from .utils import create_news_articles
from .cybersports_ru_parser import parse_cybersport_ru_news


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
