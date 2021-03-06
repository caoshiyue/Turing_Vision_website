from os import name
from django.http.response import HttpResponseBadRequest
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
from django.urls import reverse

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


def login(request, message='', next=''):
    if next == '':
        next = request.GET.get('next')
    context = {'message': message, 'next_url': next}
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
    for s in subm:
        s.ap = round(s.ap, 4)
        s.ap50 = round(s.ap50, 4)
        s.ap75 = round(s.ap75, 4)
        s.aps = round(s.aps, 4)
        s.apm = round(s.apm, 4)
        s.apl = round(s.apl, 4)
        s.timestamp = s.timestamp.date()
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
        next_url = request.POST.get('next_url')
        if next_url == 'None' or next_url == '' or next_url == '{{':
            next_url = '/user_account'
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
                return redirect(next_url)
    #! 这里用传参
    return redirect(reverse('login', kwargs={"message": message, 'next': next_url}))

# TODO: 注册,发邮件


def register_request(request):
    if request.method == "POST":
        form = register_form(request.POST)
        message = ''
        if form.is_valid():
            usr = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            a = User.objects.filter(email=email)
            b = User.objects.filter(username=usr)
            if a.count() != 0 or b.count() != 0:
                message = "用户名或邮箱已注册"
            else:
                message = "已发送确认邮件，请查收(包括垃圾邮件)"
                # password 再次hash
                User.objects.create_user(username=usr, email=email, password=password, is_active=False, date_joined=str(
                    timezone.now()), last_login=str(timezone.now()))
                send_email(usr, email)

        return HttpResponse(message, status=200)
    return HttpResponseBadRequest()


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
