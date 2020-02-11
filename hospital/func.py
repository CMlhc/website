import json
from datetime import datetime
from time import time

from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .form import photoForm
from .models import *

@csrf_exempt
def picture(request):
    if request.method == 'POST':
        form = photoForm(request.POST, request.FILES)
        if 'img' in request.FILES:
            image = request.FILES["img"]
            image.name = str(time()) + image.name
            pic = Pictures()
            pic.pic = image
            pic.save()
            return JsonResponse({'img': pic.id})
        else:
            return JsonResponse({'error': "upload image fail."})
    elif request.method == 'GET':
        if not request.GET.get('img'):
            return render(request, "hospital/index.html")
        try:
            img = Pictures.objects.get(id=request.GET.get('img', None))
        except Pictures.DoesNotExist:
            return HttpResponseNotFound()
        return HttpResponse(img.pic, content_type='image/png')

@csrf_exempt
def uploadill(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"error", "json data error."})
    must_contains = ['name', 'age', 'gender', 'ill', 'info', 'wechat']
    for x in must_contains:
        if x not in post_data:
            return JsonResponse({"error": "no {}".format(x)})
    wechat = User.objects.get(openid=post_data['wechat'])
    try:
        patient = Patient.objects.get(wechat=wechat)
    except Patient.DoesNotExist:
        patient = Patient()
        patient.wechat = wechat
        wechat.role = 2
        wechat.save()

    patient_fields = patient.json().keys()
    for x in patient_fields:
        if x in post_data and post_data[x] != getattr(patient, x):
            setattr(patient, x, post_data[x])
    patient.save()

    history = History()
    history.patient = patient
    history.ill = post_data['ill']
    history.info = post_data['info']
    history.doctor = None
    history.diag_time = None
    history.send_time = datetime.now()
    history.rank = 0
    history.save()

    if 'pics' in post_data:
        for pic in post_data['pics']:
            try:
                p = Pictures.objects.get(id=pic)
            except Pictures.DoesNotExist:
                return JsonResponse({'error': 'picture id {} does not exist.'.format(pic)})
            pt = PictureTable()
            pt.pic = p
            pt.history = history
            pt.save()

    return JsonResponse({'success': True})


def checkcode(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"error", "json data error."})
    if 'code' not in post_data:
        return JsonResponse({"error", "no code."})
    code = post_data['code']
    try:
        doctor = Doctor.objects.get(code=code)
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "invalid code"})
    token = str(uuid.uuid4())
    doctor.token = token
    doctor.save()
    return JsonResponse({"code": code, "token": token})
