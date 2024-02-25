from django.urls import path

from .views import NewsListView, NewsCreateView, NewsDetailView, subscriptions

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]