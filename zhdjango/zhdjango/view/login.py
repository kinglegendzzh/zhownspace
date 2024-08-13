from django.http import HttpResponse
from django.http import JsonResponse


def httpTest(request):
    return HttpResponse("httpTest")


def jsonTest(request):
    return JsonResponse({'a': 'b'})
