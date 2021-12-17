from os import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from image.models import *
from image.leaderboard import read_leaderboard_file, generate_leaderboard_tofile
from image.user import *
import hashlib
from django.utils import timezone
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


def login(request):
    context = {'message': ''}
    return render(request, 'auth/login.html', context)


def register(request):
    context = {'message': ''}
    return render(request, 'auth/register.html', context)


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

#todo: 保持登录


def login_request(request):
    if request.method == "POST":
        form = login_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            message = ''
            try:
                user = Users.objects.get(email=email)
                if user.password_hash == password:
                    #TODO: 用户页面
                    return redirect('/login/')
                else:
                    message = "密码不正确"
            except:
                message = "用户不存在"
        return render(request, 'auth/login.html', locals())

    form = login_form()
    return render(request, 'auth/login.html', locals())

# TODO: 注册,发邮件


def register_request(request):
    if request.method == "POST":
        form = register_form(request.POST)
        if form.is_valid():
            usr = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            message = ''
            try:
                Users.objects.get(email=email)
                Users.objects.get(username=usr)
                message = "用户名或邮箱已注册"
            except:
                message = ""
                Users.objects.create(
                    username=usr, email=email, password_hash=password, confirmed=False, registration_time=str(timezone.now()), last_seen=str(timezone.now()))
                send_email(usr, email)

        return render(request, 'auth/register.html', locals())

    form = register_form()
    return render(request, 'auth/register.html', locals())


def register_confirm(request):
    username = request.GET.get('user')
    token = request.GET.get('token')
    message = ''
    try:
        usr = Users.objects.get(username=username)
        m = hashlib.md5(usr.email.encode())
        p = m.hexdigest()
        if p == token:
            usr.confirmed = 1
            usr.save()
            message = '验证成功'
        else:
            message = '验证失败'
    except:
        message = "验证失败"
    return render(request, 'auth/confirm_result.html', locals())
