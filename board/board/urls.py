from django.contrib import admin
from django.urls import path, include
from ads.views import AdsList
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views as ckeditor_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AdsList.as_view(), name='home'),
    path('ads/', include('ads.urls')),
    path('accounts/', include("accounts.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
