from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('',views.review_list,name='home'),
    path('reviews/<genre_name>/',views.review_list,name='review_list_by_genre'),
    path('review/<int:id>/<slug>/',views.review_detail,name='review_detail'),
    path('book/<slug>/',views.book_detail,name='book_detail'),
    path('author/<int:id>/',views.author_detail,name='author_detail'),
    path('books/',views.book_list,name='book_list'),
    path('books/<genre_name>/',views.book_list,name='book_list_by_genre'),
]