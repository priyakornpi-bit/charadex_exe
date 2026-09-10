from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "hello/index.html")


def about(request):
    context = {
        "method": request.method,
        "path": request.path,
        "query": dict(request.GET),
        "user_agent": request.META.get("HTTP_USER_AGENT", "-"),
    }
    return render(request, "hello/about.html", context)
