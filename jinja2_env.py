##
# Author:
# Description:
# LastEditors: Shiyuec
# LastEditTime: 2021-12-01 15:12:07
##
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
