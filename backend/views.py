import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

import re
import time, datetime 
from backendModels.models import UrlLog, User

def index(request):
    return render(request, 'index.html')

@csrf_protect
def uploadUrlLog(request):
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
