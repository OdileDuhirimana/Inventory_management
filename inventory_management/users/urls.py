# users/urls.py
from django.urls import path
from .views import register, login_view, logout_view, home, all_users_api

urlpatterns = [
    path('', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('users/json', all_users_api, name='user_json'),
]
