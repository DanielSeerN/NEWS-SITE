from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory


from .models import SourceCategory, User, Reader, NewsArticle, FavouriteArticle
from .views import RegistrationView, LoginView, do_main_news, get_categories, get_category_news, add_favourite_article, \
    get_favourite_articles, show_article


class AppTest(TestCase):
    """
    Тесты приложения
    """
    def setUp(self) -> None:
        """
        Создание необходимых объектов для тестов
        """
        icon = SimpleUploadedFile('cybersport-ru-icon.jpg', content=b'', content_type='image/jpg')
        self.factory = RequestFactory()
        self.category = SourceCategory.objects.create(title='News.com', slug='news.com', icon=icon)
        self.article = NewsArticle.objects.create(title='article',
                                                  slug='12341adfa',
                                                  category='sports',
                                                  source=self.category,
                                                  text='article text',
                                                  post_time='22-03-22',
                                                  news_link='article.com/source')
        self.user = User.objects.create_user(username='чел', password='lol')
        self.reader = Reader.objects.create(user=self.user, mail_box='lol@kadmaf.com')

    def test_favourite_article_creation(self):
        """
        Тест создания избранной статьи
        """
        favourite_article = FavouriteArticle.objects.create(reader=self.reader, article=self.article)
        self.assertTrue(favourite_article)

    def test_registration(self):
        """
        Тест регистрации
        """
        new_user = User.objects.create_user(username='челыч', password='lolxd')
        new_user.adress = 'spb'
        new_user.phone = '+4561241342'
        reader = Reader.objects.create(user=new_user, mail_box='lolxd@dasfgsa.com')
        self.assertTrue(self.client.login(username=new_user.username, password=new_user.password))
        self.assertTrue(reader)

    def test_login(self):
        """
        Тест входа
        """
        self.assertTrue(self.client.login(username='чел', password='lol'))

    def test_response_from_registration_view(self):
        """
        Тест ответа от представления регистрации
        """
        request = self.factory.get('/registration/')
        request.user = self.user
        response = RegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_response_from_login_view(self):
        """
        Тест ответа от представления входа
        """
        request = self.factory.get('/login/')
        request.user = self.user
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_response_from_main_page(self):
        """
        Тест ответа от представления главной страницы
        """
        request = self.factory.get('')
        request.user = self.user
        response = do_main_news(request)
        self.assertEqual(response.status_code, 200)

    def test_response_from_categories_page(self):
        """
        Тест ответа от представления страницы с категорями
        """
        request = self.factory.get('')
        request.user = self.user
        response = get_categories(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, '/categories')

    def test_response_from_category_news_page(self):
        """
        Тест ответа от представления страницы со статьями с категориями
        """
        request = self.factory.get('')
        request.user = self.user
        response = get_category_news(request, slug='news.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, '/category/news.com')

    def test_response_from_favourite_articles_page(self):
        """
        Тест ответа от представления страницы с избранными статьями
        """
        request = self.factory.get('')
        request.user = self.user
        response = get_favourite_articles(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, '/fav-articles')

    def test_response_from_article_page(self):
        """
        Тест ответа от представления страницы для статьи
        """
        request = self.factory.get('')
        request.user = self.user
        response = show_article(request, slug='12341adfa')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, '/articles/12341adfa')

    def test_add_to_favourite_articles(self):
        """
        Тест представления для добавления избранной статьи
        """
        request = self.factory.get('')
        request.user = self.user
        response = add_favourite_article(request, slug='12341adfa')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/articles/12341adfa')
# Create your tests here.
