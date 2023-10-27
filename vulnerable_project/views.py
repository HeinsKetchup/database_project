from django.shortcuts import render, redirect

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    user = User.objects.filter(username=username, password=password).first()

    if user:
        return JsonResponse({"status": "logged in"})
    else:
        return JsonResponse({"status": "invalid credentials"})


def json_convert(request):
    return render(request,'json_conversion.html')
