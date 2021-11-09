from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .models import NewsArticle, FavouriteArticle, Reader
from .create_news import make_news
from .forms import LoginForm, RegistrationForm


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


def add_favourite_article(request, **kwargs):
    article_slug = kwargs.get('slug')
    user = request.user
    reader = Reader.objects.get(user=user)
    article = NewsArticle.objects.get(slug=article_slug)
    favourite_article = FavouriteArticle.objects.create(article=article, reader=reader)
    reader.favourite_articles.add(favourite_article)
    favourite_article.save()
    print(user)
    print(reader)
    print(favourite_article)
    return HttpResponseRedirect('/')


class LoginView(View):
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

# Create your views here.
