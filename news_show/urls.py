from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import CategoryPage, CategoryNewsPage, FavouriteArticlesPage, LoginView, \
    RegistrationView, ArticlePage, LeaveComment, MainPage, AddFavouriteArticle

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('categories/', CategoryPage.as_view(), name='categories'),
    path('add-to-favourites/<str:slug>/', AddFavouriteArticle.as_view(), name='add_to_favourites'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('articles/<str:slug>/', ArticlePage.as_view(), name='articles'),
    path('fav-articles/', FavouriteArticlesPage.as_view(), name='fav_articles'),
    path('category/<str:slug>', CategoryNewsPage.as_view(), name='category'),
    path('comment/<str:slug>', LeaveComment.as_view(), name='comment')

]

<<<<<<< HEAD
refresh()
=======
>>>>>>> a8b24d9ab24e88a0d04473c487e0b26a595de24c


