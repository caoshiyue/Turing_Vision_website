"""turingvision URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from image.views import *
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.views import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image/', include('image.urls', namespace='image')),
    path('', home, name='home'),
    path('train/', trainpart, name='train'),
    path('test/', testpart, name='test'),
    path('tutorial/', tutor, name='tutorial'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('contact/', contact, name='contact'),
    path('download/', download, name='download'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('user_account/', user_account, name='user_account'),
    path('login_request/', login_request, name='login_request'),
    url(r'^login/(?P<message>.*)/(?P<next>/.*)', login, name='login'),
    path('register_request/', register_request, name='register_request'),

    url(r'^next/', get),
    url(r'^number/', get_img_number),
    url(r'^anno/', save_anno),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^register_confirm/', register_confirm),
]
