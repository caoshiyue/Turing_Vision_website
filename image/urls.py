##
# Author:
# Description:
# LastEditors: Shiyuec
# LastEditTime: 2021-10-12 17:15:27
##
from image.views import home
from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
import image.views as views

# App名称
# 用于Django幕后的url查询
app_name = 'image'

# url列表
urlpatterns = [
    # path('', home, name='home'),

]
