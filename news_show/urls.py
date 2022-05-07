from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import get_categories, do_main_news, add_favourite_article, LoginView, \
    RegistrationView, show_article, get_favourite_articles, get_category_news, leave_a_comment
from .news_refresher import refresh
urlpatterns = [
    path('', do_main_news, name='main'),
    path('categories/', get_categories, name='categories'),
    path('add-to-favourites/<str:slug>/', add_favourite_article, name='add_to_favourites'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('articles/<str:slug>/', show_article, name='articles'),
    path('fav-articles/', get_favourite_articles, name='fav_articles'),
    path('category/<str:slug>', get_category_news, name='category'),
    path('comment/<str:slug>', leave_a_comment, name='comment')

]

# refresh()


