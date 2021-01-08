from collections import namedtuple
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('warzone', views.warzone, name='warzone'),
    path('friends', views.friends, name='friends'),
    path('history', views.history, name='history')
]