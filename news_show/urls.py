from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import get_cybersport_ru_news, get_cyber_sport_ru_news, do_main_news, add_favourite_article, LoginView, RegistrationView
urlpatterns = [
    path('', do_main_news, name='main'),
    path('cybersport-ru/', get_cybersport_ru_news , name='cybersport_ru'),
    path('cyber-sport-ru/', get_cyber_sport_ru_news , name='cyber_sport_ru'),
    path('add-to-favourites/<str:slug>/', add_favourite_article, name='add_to_favourites'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
   path('logout/', LogoutView.as_view(), name='logout'),
]