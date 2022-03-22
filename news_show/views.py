from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .models import NewsArticle, FavouriteArticle, Reader, SourceCategory
from .forms import LoginForm, RegistrationForm


def do_main_news(request):
    """
    Главная страница агрегатора.
    """
    all_news = NewsArticle.objects.order_by('post_time')
    context = {
        'all_news': all_news
    }
    return render(request, 'news_show/index.html', context)


def get_categories(request):
    """
    Представление для категорий новостей.
    """
    categories = SourceCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'news_show/categories.html', context)


def get_category_news(request, **kwargs):
    """
    Представление для новостей категории.
    """
    category = SourceCategory.objects.get(slug=kwargs.get('slug'))
    news = NewsArticle.objects.filter(source=category)
    context = {
        'news': news,
        'category': category
    }
    return render(request, 'news_show/category_news.html', context)


def add_favourite_article(request, **kwargs):
    """
    Представление для добавления новости в избранное
    """
    article_slug = kwargs.get('slug')
    user = request.user
    reader = Reader.objects.get(user=user)
    article = NewsArticle.objects.get(slug=article_slug)
    favourite_article, created = FavouriteArticle.objects.get_or_create(article=article, reader=reader)
    if created:
        pass
    else:
        reader.favourite_articles.add(favourite_article)
        favourite_article.save()
    return HttpResponseRedirect('/')


def get_favourite_articles(request):
    """
    Представление для отображения избранных новостей пользователя.
    """
    user = request.user
    reader = Reader.objects.get(user=user)
    reader_favourites = FavouriteArticle.objects.filter(reader=reader)
    context = {
        'favourites': reader_favourites
    }
    return render(request, 'news_show/reader_fav_articles.html', context)


def show_article(request, **kwargs):
    """
    Представление для отображения статьи.
    """
    article_slug = kwargs.get('slug')
    article = NewsArticle.objects.get(slug=article_slug)
    article_text = article.text.split('*')
    context = {
        'article': article,
        'article_text': article_text
    }
    return render(request, 'news_show/article.html', context)


class LoginView(View):
    """
    Представление для входа в учётную запись.
    """

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)

        context = {
            'form': form
        }

        return render(request, 'news_show/login.html', context)

    def post(self, request, *args, **kwargs):
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

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'news_show/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.save()
            reader = Reader.objects.create(user=user, mail_box=user.email)
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('/')
        context = {
            'form': form
        }

        return render(request, 'news_show/registration.html', context)
