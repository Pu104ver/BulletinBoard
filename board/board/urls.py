from django.contrib import admin
from django.urls import path, include
from ads.views import AdsList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AdsList.as_view()),
    path('ads/', include('ads.urls')),
    # path('accounts/', include("allauth.urls")),
    path('accounts/', include("accounts.urls")),

]
