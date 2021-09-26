import os
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.conf import settings

USER = get_user_model()


def images_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'images')


class LatestNewsManager:
    @staticmethod
    def get_latest_news(*args, **kwargs):
        news = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            news_models = ct_model.model_class().objects.all().order_by('-id')[:5]
            news.extend(news_models)
        return news


class LatestNews:
    objects = LatestNewsManager()


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self, vievname):
        ct_model = self.__class__._meta.model_name
        return reverse(vievname, kwargs={'ct_model': ct_model, 'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Category'


class NewsArticle(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    category = models.CharField(max_length=255, verbose_name='Тема')
    news_link = models.CharField(max_length=255, verbose_name='Ссылка на статью')
    post_time = models.CharField(max_length=255, verbose_name='Время выкладывания')


class Reader(models.Model):
    name = models.ForeignKey(USER, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    mail_box = models.CharField(max_length=255, verbose_name='Почта пользователя', null=True)

    def __str__(self):
        return f'Читатель {self.name.first_name}'
