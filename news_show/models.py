import os
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.urls import reverse
from django.conf import settings

User = get_user_model()



class FavouriteArticle(models.Model):
    article = models.ForeignKey('NewsArticle', verbose_name='Избранная новость', on_delete=models.CASCADE, null=True)
    reader = models.ForeignKey('Reader', verbose_name='Читатель', on_delete=models.CASCADE)


class NewsArticle(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    category = models.CharField(max_length=255, verbose_name='Тема')
    news_link = models.CharField(max_length=255, verbose_name='Ссылка на статью')
    post_time = models.CharField(max_length=255, verbose_name='Время выкладывания')
    slug = models.SlugField(unique=True)
    source = models.CharField(max_length=255, verbose_name='Источник')


    def __str__(self):
        return self.title


class Reader(models.Model):
    user = models.ForeignKey(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    mail_box = models.CharField(max_length=255, verbose_name='Почта пользователя', null=True)
    favourite_articles = models.ManyToManyField(FavouriteArticle, blank=True, related_name='favourite_articles')

    def __str__(self):
        return f'Читатель {self.user.username}'
