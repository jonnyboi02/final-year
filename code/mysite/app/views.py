from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
import io, json
from django.contrib.auth import authenticate, login
import os
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def register(request):
    json_data = request.body
    body = json.loads(json_data)
    #query_seller = body['seller']
    username = body['username']
    password = body['password']
    for user in User.objects.filter(username = username):
        if user.username == username:
            return HttpResponse(status = 400)
    user = User.objects.create_user(username)
    user.set_password(password)
    user.save()
    return HttpResponse(status  = 200)
    #return HttpResponse("Hi")

def login(request):
    json_data = request.body
    body = json.loads(json_data)
    #query_seller = body['seller']
    username = body['username']
    password = body['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        return redirect
    else:
        pass

#create view that makes use of Geth API call, done probably by OS calls
