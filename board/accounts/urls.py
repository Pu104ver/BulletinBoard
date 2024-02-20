from django.urls import path
from .views import register, confirm_code, login_user, logout_user

urlpatterns = [
    path('signup/', register, name='register'),
    path('confirm_code/', confirm_code, name='confirm_code'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
