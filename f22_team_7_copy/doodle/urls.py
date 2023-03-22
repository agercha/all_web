"""doodle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from doodleio import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.login_action, name="home"),
    path('waitingroom', views.waiting, name='waitingroom'),
    path('try-enter', views.try_enter, name='try-enter'),
    path('game', views.game_action, name="game"),
    path('leaderboard', views.leaderboard, name="leaderboard"),
    path('gameover', views.game_over, name="gameover"),
    path('new-round', views.new_round, name="new-round"),
    path('add-chat', views.add_chat, name='ajax-add-chat'),
    path('get-chat', views.get_chat_json_dumps_serializer),
    path('get-users', views.get_users),
    path('get-users-leaderboard', views.get_users_leaderboard)
]
