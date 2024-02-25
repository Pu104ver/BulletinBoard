from django.urls import path, include
from django.views.decorators.cache import cache_page

from news.views import subscriptions
from .views import AdsList, AdsDetail, MyPostsListView, AdCreateView, AdUpdateView, AdDeleteView, SubmitResponseView, \
    MyResponsesListView, MyResponsesToAdsListView, ResponseDeleteView, accept_response

urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('<int:pk>', AdsDetail.as_view(), name='ads_detail'),
    path('my-posts', MyPostsListView.as_view(), name='my_posts'),
    path('create/', AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    path('<int:ad_id>/submit_response/', SubmitResponseView.as_view(), name='submit_response'),
    path('my-responses/', MyResponsesListView.as_view(), name='my_responses'),
    path('responses-to-me/', MyResponsesToAdsListView.as_view(), name='responses_to_my_ads'),
    path('my-responses/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response_delete'),
    path('responses/<int:pk>/accept_response/', accept_response, name='accept_response'),
]