from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register, confirm_code

urlpatterns = [
    path('signup/', register, name='register'),
    path('confirm_code/', confirm_code, name='confirm_code'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]
