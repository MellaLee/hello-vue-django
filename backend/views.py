import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import ast
import re
import json
import time, datetime 
import numpy as np
from backendModels.models import UrlLog, User, QuantitativeLog

import pandas as pd

http_response_obj = {}
http_response_obj['code'] = 0
http_response_obj['data'] = None 
http_response_obj['msg'] = ''

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def uploadUrlLog(request):
    if request.method == 'POST':
        fname = request.FILES.get('file')
        if fname:
            user, created = User.objects.get_or_create(
                userNo=fname.name.split('.')[0].split('-')[1])
            if (created):
                user.save()
            file = open('static/upload/' + fname.name, 'wb')
            for chunk in fname.chunks():
                file.write(chunk)
            file.close()
            return HttpResponse('OK')


@csrf_exempt
def uploadUrlLogOld(request):
    if request.method == 'POST':
        fileName = request.FILES.get('file')
        invalidData = 0
        if fileName:
            for row in fileName:
                try:
                    data = re.split(r',(?!(?:(?:(?!,)(?!").)*,)*(?:(?!,)(?!").)+")', row.decode('gbk'))
                    user, created = User.objects.get_or_create(
                        userNo=data[0], ip=data[3])
                    if (created):
                        user.save()
                    y, m, d, h, M = (time.strptime(
                        data[7].strip('\r\n'), "%Y/%m/%d %H:%M"))[0: 5]
                    urlLog = UrlLog(
                        user_id=user.id,
                        url=data[4],
                        urlArgs=data[6],
                        time=datetime.datetime(y, m, d, h, M, 0, 0)
                    )
                    urlLog.save()
                except Exception as e:
                    print (e, row)
                    invalidData += 1
            print ('无效数据共', invalidData , '条.')
            return HttpResponse('OK')

def chartShow(request):
    series = {}
    for item in QuantitativeLog.objects.order_by('-similarEuc')[:10]:
       series[item.url] = {
           'x': json.loads(item.timeSeries),
           'y': json.loads(item.urlSimilarOriginSeries)
       }
        
    return render(request, 'chart.html', {'series': series})

@csrf_exempt
def fetchUrlList(request):
    data = {}
    series = QuantitativeLog.objects
    data['total'] = series.count()
    intParams = changeRequestIntoInt(request)
    start = ( intParams['page'] - 1 ) * intParams['size']
    end = intParams['page'] * intParams['size']
    data['list'] = list(series.all()[start:end].values('user', 'url', 'similarEuc', 'urlArgsEntropy', 'abnormalTimeProbability', 'sameArgsDiversity', 'webClassify'))
    http_response_obj['data'] = data
    return JsonResponse(http_response_obj)

def changeRequestIntoInt(request):
    result = {}
    params = request.GET
    for item in params:
        if params[item] is not None and params[item].isnumeric():
            result[item] = int(params[item])
        else:
            result[item] = params[item]
    return result

@csrf_exempt
def fetchLabelList(request):
    # autoMark()
    # return
    data = {}
    series = UrlLog.objects.filter(mark=1)
    data['total'] = series.count() 
    intParams = changeRequestIntoInt(request)
    start = ( intParams['page'] - 1 ) * intParams['size']
    end = intParams['page'] * intParams['size']
    data['list'] = list(series[start:end].values('url', 'user_id', 'times', 'urlArgs', 'id'))
    http_response_obj['data'] = data
    return JsonResponse(http_response_obj)

# 自动标记函数，默认访问次数总和<10的访问为善意访问，mark置为0
def autoMark():
    allModel = UrlLog.objects.filter(mark=1)
    whilelist = ['qq.com', 'weixin.com', 'baidu.com', 'duba.net', 'sogou.com', 'ludashi', 'msg.71.am', 'cmcm.com', 'alibaba.com', '360.cn', 'sina', 'youdao.com', 'rising.com.cn', 'alicdn.com', 'aliyun.com', 'huajiao.com', 'ijinshan.com', '163.com', 'api.foxitreader.cn', 'api.mi.wifi.com', 'wx.qlogo.cn']
    for i in range(1, 31):
        model = allModel[((i - 1) * 10000) : (10000 * i)]
        # p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        for item in model:
            # for wl in whilelist:
            #     if (wl in item.url):
            #         item.mark = 0
            #         item.save()
            #         print (item.id)
            #         continue
            # else:
            #     times = ast.literal_eval(item.times) 
            #     total = 0
            #     for i in times:
            #         if (i > 0):
            #             total+=1
            #     if (total < 20):
            # if p.match(item.url):
            if (item.url != 'stat.funshion.net'):
                item.mark = 0
                item.save()
                print (item.id)

@csrf_exempt
def saveLabel(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        for item in body['label']:
            QuantitativeLog.objects.filter(user_id=item['user_id'], url=item['url']).update(label=item['label'])
            UrlLog.objects.filter(id=item['id']).update(mark=0)
    http_response_obj['data'] = 'ok'
    return JsonResponse(http_response_obj)