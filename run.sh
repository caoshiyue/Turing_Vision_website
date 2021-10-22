#! /bin/bash
##上线修改
python3 manage.py collectstatic
uwsgi --ini /home/webtest2_v4/uwsgi.ini & /usr/sbin/nginx