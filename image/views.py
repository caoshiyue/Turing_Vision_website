from os import name
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from image.models import *
from image.leaderboard import read_leaderboard_file, generate_leaderboard_tofile
# Create your views here.


def home(request):
    context = {}
    return render(request, 'index.html', context)


def tutor(request):
    context = {}
    return render(request, 'tutorial.html', context)


def trainpart(request):
    context = {}
    return render(request, 'train.html', context)


def testpart(request):
    context = {}
    return render(request, 'test.html', context)


def leaderboard(request):
    generate_leaderboard_tofile()
    context = read_leaderboard_file()
    return render(request, 'leaderboard.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)


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


def download(request):
    try:
        file = 'static/test_data/test.zip'
        response = StreamingHttpResponse(file_iterator(file))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="main.zip"'
        print(response)
    except:
        print("cannot read")
    return response


def file_iterator(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
