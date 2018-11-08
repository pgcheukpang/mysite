from django.shortcuts import render
from django.utils.decorators import method_decorator


def index(request):
    return render(request, "home/loveliving.html")


def baidu_map(request):
    return render(request, "home/baidu.html")


def contact(request):
    # print(request.session.items())
    return render(request, "home/contact.html")
