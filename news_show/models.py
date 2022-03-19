from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()  # Для пользователей испоьзуем встроенную модель джанго


class SourceCategory(models.Model):
    """
    Модель категории по источнику
    """
    title = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    icon = models.ImageField(verbose_name='Изображение')

    def __str__(self):
        return self.title


class FavouriteArticle(models.Model):
    """
    Модель для избранной статьи
    """
    article = models.ForeignKey('NewsArticle', verbose_name='Избранная новость', on_delete=models.CASCADE, null=True)
    reader = models.ForeignKey('Reader', verbose_name='Читатель', on_delete=models.CASCADE)


class NewsArticle(models.Model):
    """
    Модель для статьи
    """
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    category = models.CharField(max_length=255, verbose_name='Тема')
    news_link = models.CharField(max_length=255, verbose_name='Ссылка на статью')
    post_time = models.CharField(max_length=255, verbose_name='Время выкладывания')
    slug = models.SlugField(unique=True)
    source = models.ForeignKey(SourceCategory, max_length=255, verbose_name='Источник', on_delete=models.CASCADE)
    text = models.TextField(default='text', verbose_name='Текст статьи')

    def get_absolute_url(self):
        return reverse('articles', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Reader(models.Model):
    """
    Модель для читателя
    """
    user = models.ForeignKey(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    mail_box = models.CharField(max_length=255, verbose_name='Почта пользователя', null=True)
    favourite_articles = models.ManyToManyField(FavouriteArticle, blank=True, related_name='favourite_articles')

    def __str__(self):
        return f'Читатель {self.user.username}'
