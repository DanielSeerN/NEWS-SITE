from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .models import FavouriteArticle, Reader, Comment
from .forms import LoginForm, RegistrationForm, CommentForm
from .services import get_reader, get_article_by_slug, get_category, get_articles_by_category, get_all_categories, \
    get_all_news, get_favorite_articles


class MainPage(View):
    """
    Главная страница агрегатора.
    """

    def get(self, request):
        all_news = get_all_news()
        context = {
            'all_news': all_news
        }
        return render(request, 'news_show/index.html', context)


class CategoryPage(View):
    """
    Представление для категорий новостей.
    """

    def get(self, request):
        categories = get_all_categories()
        context = {
            'categories': categories
        }
        return render(request, 'news_show/categories.html', context)


class CategoryNewsPage(View):
    """
    Представление для новостей категории.
    """

    def get(self, request, **kwargs):
        category = get_category(kwargs)
        news = get_articles_by_category(category)
        context = {
            'news': news,
            'category': category
        }
        return render(request, 'news_show/category_news.html', context)


class AddFavouriteArticle(View):
    def post(self, request, **kwargs):
        """
        Представление для добавления новости в избранное
        """
        article = get_article_by_slug(kwargs)
        reader = get_reader(request)
        favourite_article, created = FavouriteArticle.objects.get_or_create(article=article, reader=reader)
        if created:
            pass
        else:
            reader.favourite_articles.add(favourite_article)
            favourite_article.save()
        return HttpResponseRedirect('/')


class FavouriteArticlesPage(View):
    """
    Представление для отображения избранных новостей пользователя.
    """

    def get(self, request):
        reader = get_reader(request)
        reader_favourites = get_favorite_articles(reader)
        context = {
            'favourites': reader_favourites
        }
        return render(request, 'news_show/reader_fav_articles.html', context)


class ArticlePage(View):
    def get(self, request, **kwargs):
        """
        Представление для отображения статьи.
        """
        article = get_article_by_slug(kwargs)
        article_text = article.text.split('*')
        form = CommentForm(request.POST or None)
        comments = Comment.objects.filter(article=article)
        context = {
            'article': article,
            'article_text': article_text,
            'form': form,
            'comments': comments
        }
        return render(request, 'news_show/article.html', context)


class LeaveComment(View):
    def get(self, request, **kwargs):
        """
        Представление для создания комментария
        """
        article = get_article_by_slug(kwargs)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text']
            reader = get_reader(request)
            Comment.objects.create(text=comment_text, reader=reader, article=article)
        return HttpResponseRedirect(f'/articles/{article.slug}')


class LoginView(View):
    """
    Представление для входа в учётную запись.
    """

    def get(self, request):
        form = LoginForm(request.POST or None)

        context = {
            'form': form
        }

        return render(request, 'news_show/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
        context = {
            'form': form
        }

        return render(request, 'news_show/login.html', context)


class RegistrationView(View):
    """
    Представление для регистрации учётной записи.
    """

    def get(self, request):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'news_show/registration.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.save()
            Reader.objects.create(user=user, mail_box=user.email)
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('/')
        context = {
            'form': form
        }

        return render(request, 'news_show/registration.html', context)
