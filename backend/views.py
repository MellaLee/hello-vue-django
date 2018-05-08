import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request, 'index.html')

@csrf_protect
def uploadUrlLog(request):
    if request.method == 'POST':
        BASE_DIR = os.path.abspath('.') + '/static/'
        obj = request.FILES.get('file')
        print(os.path.join(BASE_DIR, obj.name))
        f = open(os.path.join(BASE_DIR, obj.name), 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse('OK')
