#! /bin/bash
##上线修改
python3 manage.py collectstatic
uwsgi --ini /home/vision_turing_web_v9/uwsgi.ini & /usr/sbin/nginx