##
# Author:
# Description:
# LastEditors: Shiyuec
# LastEditTime: 2021-12-26 19:49:38
##
from os import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from image.models import *
from image.leaderboard import read_leaderboard_file, generate_leaderboard_tofile
from image.user import *
import hashlib
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login as login_keep
from django.contrib.auth import logout as logout_keep
from django.contrib.auth.decorators import login_required

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


@login_required
def testpart(request):
    context = {}
    return render(request, 'test.html', context)


def leaderboard(request):
    # TODO： 生成file 放在eval处
    generate_leaderboard_tofile()
    context = read_leaderboard_file()
    return render(request, 'leaderboard.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)


def login(request):
    action = request.GET.get('action')
    if action == 'login_request/':
        return login_request(request)
    else:
        next_url = request.GET.get('next')
        context = {'message': '', 'next_url': next_url}
        return render(request, 'auth/login.html', context)


@login_required
def logout(request):
    context = {}
    logout_keep(request)
    return redirect('/')


def register(request):
    context = {'message': ''}
    return render(request, 'auth/register.html', context)


@login_required
def user_account(request):
    user = request.user
    subm = user.submissions_set.all()
    context = {'submission': subm}
    return render(request, 'auth/user_account.html', context)


def get(request):
    context = {}
    # 通过request.GET['name']形式获取get表单内容
    # result为重定向到的result.html所使用的变量
    user = request.user.username
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
    user = request.user.username
    p = request.GET.get('p')
    if p == 'train':
        result = get_train_number()
    else:
        result = get_number(user, int(p))
    return HttpResponse(result, content_type="application/json")


def save_anno(request):
    user = request.user.username
    data = json.loads(request.body)
    do_save_anno(data, user)
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
        message = ''
        next_url = 'None'
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate_email(
                request, email, password)
            if user == None:
                message = "用户名或密码不正确"
            elif not user.is_active:
                message = "邮箱未验证"
            else:
                login_keep(request, user)
                next_url = request.POST.get('next_url')
                if next_url == 'None' or next_url == '' or next_url == '{{':
                    #todo: 用户界面
                    return redirect('/user_account')
                else:
                    return redirect(next_url)

    form = login_form()
    return render(request, 'auth/login.html', {'message': message})

# TODO: 注册,发邮件


def register_request(request):
    if request.method == "POST":
        form = register_form(request.POST)
        message = ''
        if form.is_valid():
            usr = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                User.objects.get(email=email)
                User.objects.get(username=usr)
                message = "用户名或邮箱已注册"
            except:
                message = ""
                # password 再次hash
                User.objects.create_user(username=usr, email=email, password=password, is_active=False, date_joined=str(
                    timezone.now()), last_login=str(timezone.now()))
                send_email(usr, email)

        return render(request, 'auth/register.html', locals())

    form = register_form()
    return render(request, 'auth/register.html', locals())


def register_confirm(request):
    username = request.GET.get('user')
    token = request.GET.get('token')
    message = ''
    try:
        usr = User.objects.get(username=username)
        m = hashlib.md5(usr.email.encode())
        p = m.hexdigest()
        if p == token:
            usr.is_active = 1
            usr.save()
            message = '验证成功'
        else:
            message = '验证失败'
    except:
        message = "验证失败"
    return render(request, 'auth/confirm_result.html', locals())
