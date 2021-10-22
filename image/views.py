from os import name
from django.shortcuts import render
from django.http import HttpResponse
from image.models import *

# Create your views here.


def home(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'index.html', context)


def tutor(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'tutorial.html', context)


def trainpart(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'train.html', context)


def testpart(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'test.html', context)


def get(request):
    context = {}
    # 通过request.GET['name']形式获取get表单内容
    # result为重定向到的result.html所使用的变量
    user = request.GET.get('user')
    imgid = request.GET.get('imgid')
    p = request.GET.get('p')
    if p == 'train':
        result = get_train_image(imgid)
    else:
        result = get_image(user, int(p), imgid)
    return HttpResponse(result, content_type="application/json")


def get_img_number(request):
    context = {}
    # 通过request.GET['name']形式获取get表单内容
    # result为重定向到的result.html所使用的变量
    user = request.GET.get('user')
    p = request.GET.get('p')
    if p == 'train':
        result = get_train_number()
    else:
        result = get_number(user, int(p))
    return HttpResponse(result, content_type="application/json")


def save_anno(request):
    data = json.loads(request.body)
    do_save_anno(data)
    return HttpResponse('Success', content_type="application/json")
