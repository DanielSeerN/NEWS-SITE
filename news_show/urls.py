from django.urls import path
from .views import get_cybersport_ru_news, get_cyber_sport_ru_news, do_main_news
urlpatterns = [
    path('', do_main_news, name='main'),
    path('cybersport-ru', get_cybersport_ru_news , name='cybersport_ru'),
    path('cyber-sport-ru', get_cyber_sport_ru_news , name='cyber_sport_ru')
]