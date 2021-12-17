#! /bin/bash
##上线修改
python3 manage.py collectstatic
uwsgi --ini /home/turingvision_v9/uwsgi.ini & /usr/sbin/nginx