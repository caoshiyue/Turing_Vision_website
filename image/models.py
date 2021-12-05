from django.db import models

# Create your models here.
from django.utils.timezone import now
from image.img_json import img_json
import os
import random
import json
import re
num_datalist = 2


def read_list():
    d = []
    for i in range(num_datalist+1):
        path = 'static/datalist'+str(i)+'.txt'
        f = open(path)
        d.append(f.read().splitlines())
    return d


def read_anno():
    json_path = 'static/annotation.json'
    with open(json_path, encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data


print(os.getcwd())
datalists = read_list()
annotation = read_anno()
save_path = 'static/save'


def get_hash(user, times):
    return (hash(user)+times) % num_datalist


def deal_random(image_path):
    image = os.listdir(image_path)
    path = random.sample(image, 1)
    path = os.path.join(image_path, path[0])
    return path


def get_anno(image_path):
    anno_list = annotation[image_path]
    label = random.sample(anno_list, 1)[0].copy()
    del label['bbox']
    return label


def get_image(user, p, id):
    if p >= num_datalist:
        return
    part = get_hash(user, p)
    id = int(id)
    image_path = datalists[part][id]
    label = get_anno(image_path)
    image_path = os.path.join('static', image_path)
    path = deal_random(image_path)
    return img_json(path, label)


def get_train_image(id):
    id = int(id)
    image_path = datalists[num_datalist][id]
    image_path = os.path.join('static', image_path)
    return img_json(image_path)


def get_train_number():
    num = len(datalists[num_datalist])
    return str(num)


def get_number(user, p):
    if p >= num_datalist:
        return
    part = get_hash(user, p)
    num = len(datalists[part])
    return str(num)


def clean_file_name(filename: str):
    invalid_chars = '[\\\/:*?"<>|]'
    replace_char = '-'
    return re.sub(invalid_chars, replace_char, filename)


def do_save_anno(data):
    usr = data['usr']
    usr = clean_file_name(usr)
    usr_file = os.path.join(save_path, usr)
    del data['usr']
    if not os.path.exists(usr_file):
        os.mkdir(usr_file)
    else:
        l = len(os.listdir(usr_file))
        json_file = os.path.join(usr_file, usr)+str(l)+'.json'
        with open(json_file, "w+") as f:
            json.dump(data, f)
