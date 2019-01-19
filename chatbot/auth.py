from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Avatar


def signup(request):
    if request.method != 'POST':
        return HttpResponseForbidden()
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username:
        return JsonResponse({'result': 'error', 'msg': 'no username'})
    if not password:
        return JsonResponse({'result': 'error', 'msg': 'no password'})
    query = User.objects.filter(username=username)
    if len(query) > 0:
        return JsonResponse({'result': 'error', 'msg': '该用户已经存在'})
    user = User.objects.create_user(username=username, password=password)
    auth.login(request, user)
    default_avatar = Avatar()
    default_avatar.user = user
    default_avatar.save()
    return JsonResponse({'result': 'success', 'uid': user.id})


def signin(request):
    if request.method != 'POST':
        return HttpResponseForbidden()
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username:
        return JsonResponse({'result': 'error', 'msg': 'no username'})
    if not password:
        return JsonResponse({'result': 'error', 'msg': 'no password'})

    user = auth.authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'result': 'error', 'msg': '用户名或密码错误'})
    auth.login(request, user)
    return JsonResponse({'result': 'success', 'uid': user.id})


def logout(request):
    if request.method != 'POST':
        return HttpResponseForbidden()
    auth.logout(request)
    return JsonResponse({'result': 'success'})


def changePsw(request):
    if request.method != 'POST':
        return HttpResponseForbidden()
    old_psw = request.POST.get('old_psw')
    new_psw = request.POST.get('new_psw')
    if not old_psw:
        return JsonResponse({'result': 'error', 'msg': 'no old password'})
    if not new_psw:
        return JsonResponse({'result': 'error', 'msg': 'no new password'})

    user = request.user
    if not user.check_password(old_psw):
        return JsonResponse({'result': 'error', 'msg': '旧密码错误'})
    user.set_password(new_psw)
    user.save()
    return JsonResponse({'result': 'success', 'uid': user.id})


def changeAvatar(request):
    if request.method != 'POST':
        return HttpResponseForbidden()

    image = request.FILES.get("upload-avatar", None)
    if image is None:
        return JsonResponse({'error': 'No File'})

    # 修改文件名字
    image.name = str(request.user) + '.' + image.name.split('.')[-1]
    a = request.user.avatar
    a.avatar = image
    a.save()
    return JsonResponse({})
