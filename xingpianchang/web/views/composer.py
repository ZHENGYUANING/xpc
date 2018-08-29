from hashlib import md5
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from web.models import Post, Composer, Code
from web.helpers.utils import multi_encrypt


def oneuser(request, cid):
    composer = Composer.objects.get(cid=cid)
    composer.recent_posts = composer.posts[:2]
    return render(request, 'oneuser.html', locals())


def homepage(request, cid):
    composer = Composer.objects.get(cid=cid)
    first_post, *rest_posts = composer.posts
    return render(request, 'homepage.html', locals())


def register(request):
    return render(request, 'register.html')


def send_code(request):
    """发送手机验证码"""
    # 接受的参数
    # is_register: 1
    # phone: 13601058935
    # prefix_code: +86
    phone = request.POST.get('phone')
    
    composer = Composer.objects.filter(phone=phone).first()
    if composer:
        return JsonResponse({"status":-1025,"msg":"该手机号已注册过"})
    # 发送短信验证码
    code = Code()
    code.phone = phone
    code.created_at = datetime.now()
    code.ip = request.META.get('REMOTE_ADDR')
    code.gen_code()
    code.save()
    # 返回json
    return JsonResponse({
            "status": 0,
            "msg": "OK",
            "data": {
                 "phone": phone,
                 "prefix_code": "+86"}})
def do_register(request):
    # nickname: sssss
    # phone: 13136130957
    # code: 432424
    # password: 432443
    # prefix_code: +86
    nickname = request.POST.get('nickname')
    phone = request.POST.get('phone')
    code = request.POST.get('code')
    password = request.POST.get('password')
    co = Code.objects.filter(phone=phone, code=code).first()
    if not co:
        return JsonResponse({"status":-1,"msg":"手机验证失败"})
    delay = (datetime.now() - co.created_at.replace(tzinfo=None)).total_seconds()
    # 如果验证码超过10分钟，则也视为失败
    if delay > 60 * 10:
        return JsonResponse({"status":-1,"msg":"手机验证失败"})
    composer = Composer()
    composer.cid = composer.phone = phone
    composer.name = nickname
    composer.password = multi_encrypt(password, phone)
    composer.save()
    return JsonResponse({
        "status": 0,
        "msg": "手机验证成功",
        "data": {
            "callback": "/show_list/",
        }
    })



def login(request):
    return render(request, 'login.html')


def do_login(request):
    # prefix_code: +86
    # type: phone
    # value: 13136130957
    # password: sfsdfsa
    phone = request.POST.get('value')
    password = request.POST.get('password')
    composer = Composer.objects.filter(phone=phone).first()
    if not composer:
        return JsonResponse({"status":-1,"msg":"用户名或密码错误"})
    if composer.password != multi_encrypt(password, phone):
        return JsonResponse({"status":-1,"msg
        "data": {":"用户名或密码错误"})
    return JsonResponse({
        "status": 0,
        "msg": "登录成功",
            "callback": "/show_list/",
        }
    })
