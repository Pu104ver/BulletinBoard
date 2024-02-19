from django.contrib import admin
from django.urls import path, include
from ads.views import AdsList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AdsList.as_view()),
]
