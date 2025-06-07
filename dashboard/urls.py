from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch-tweets/', views.fetch_tweets, name='fetch_tweets'),
    path('tweet/', views.post_tweet, name='post_tweet'),
]
