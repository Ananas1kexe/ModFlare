from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('user_info', views.user_info, name='user_info'),
    path('auth/login/', views.discord_login, name='discord_login'),
    path('auth/redirect/', views.discord_callback, name='discord_callback'),
    path('auth/logout/', views.logout_view, name='logout'),

]
