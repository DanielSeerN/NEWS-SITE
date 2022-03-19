from .services import make_news


def refresh():
    """
    Функция вызова create_news.
    """
    make_news()


if __name__ == '__main__':
    make_news()
