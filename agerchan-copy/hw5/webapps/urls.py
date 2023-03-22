"""webapps URL Configuration

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
from socialnetwork import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.global_stream, name='home'),
    path('global_post', views.global_stream_post, name='global_post'),
    path('global_comment', views.global_stream_comment, name='global_comment'),
    path('self', views.users_profile, name='self'),
    path('get_self_pfp', views.get_self_pfp, name='get_self_pfp'),
    path('get_pfp/<str:author>', views.get_pfp, name='get_pfp'),
    path('get_profile/<str:author>', views.other_profile, name='get_profile'),
    path('follow_unfollow/<str:other_username>', views.follow_unfollow, name='follow_unfollow'),
    path('friend', views.friend_stream),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
]
