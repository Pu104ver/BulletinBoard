from django.contrib import admin
from django.urls import path, include
from ads.views import AdsList

app_name = 'board'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AdsList.as_view()),
    path('ads/', include('ads.urls')),
    path('accounts/', include("accounts.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
