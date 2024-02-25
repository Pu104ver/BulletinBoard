from ckeditor_uploader.views import upload, browse
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.decorators.cache import never_cache

from ads.views import AdsList
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AdsList.as_view(), name='home'),
    path('ads/', include('ads.urls')),
    path('accounts/', include("accounts.urls")),
    path('news/', include("news.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^upload/', login_required(upload), name='ckeditor_upload'),
    re_path(r'^browse/', login_required(never_cache(browse)), name='ckeditor_browse'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
