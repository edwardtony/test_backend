from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from rest_framework.parsers import JSONParser
from passlib.hash import pbkdf2_sha256
from django.http import HttpResponse
from django.conf import settings
from mailjet_rest import Client
from user.serializers import *
from user.models import *
import requests
import random
import json
import jwt

import os



# Create your views here.


#-------------------------------GLOBAL VARIABLES-------------------------------





#-------------------------------UTILS-------------------------------

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super(JSONResponse, self).__init__(content,**kwargs)

def consoleLog(text='Información',data= ''):
    print('########## {text} : {data} ##########'.format(text=text, data=data))


def generate_identifier():
    identifier = str(random.randint(1000000000,9999999999))
    try:
        Agent.objects.get(identifier = identifier)
        return generate_identifier(identifier)
    except Agent.DoesNotExist as e:
        return identifier

def generate_token(user):
    payload = {
        "phone": user['phone'],
        "identifier": user['identifier'],
        "authority": False
    }
    encoded = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    return encoded.decode("utf-8")

#--------------------------------------------- AGENT ---------------------------------------------

@csrf_exempt
def register(request):

    if request.method == 'POST':
        user = JSONParser().parse(request)
        print(user)

        user['password'] = pbkdf2_sha256.encrypt(user['password'],rounds=12000,salt_size=32)
        user['identifier'] = generate_identifier()
        user['token'] = generate_token(user)
        print(len(user['token']))

        serializer = AgentSerializer(data=user)

        if serializer.is_valid():
            try:
                validate_email(user['email'])
            except ValidationError as e:
                return JSONResponse(e, status=404)
            serializer.save()
            user_return = Agent.objects.get(pk= serializer.data['id'])
            return JSONResponse(user_return.as_dict_agent(), status=201)
        return JSONResponse(serializer.errors, status=404)
    return HttpResponse(status=404)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        credentials = JSONParser().parse(request)
        try:
            user = Agent.login(credentials)
            # user_dict = user.as_dict_user()
            # return JSONResponse(user_dict)
            token = user.token
            return JSONResponse({'token':token})
        except Agent.DoesNotExist as e:
            return HttpResponse(status=404)

@csrf_exempt
def user_info(request):
    if request.method == 'GET':
        if 'HTTP_AUTHORIZATION' not in request.META: return HttpResponse(status=403)

        try:
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
            user = Agent.objects.get(token=token)
            return JSONResponse(user.as_dict_agent())
        except Exception as e:
            print(e)
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)

#---------------------------------SOLICITUDE-------------------------------------
@csrf_exempt
def solicitude_list(request, identifier):
    """
    List all code request, or create a new request.
    """
    try:
        user = Agent.objects.get(identifier=identifier)
    except Agent.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        solicitudes = user.request_set.filter()
        solicitudes_dict = [solicitude.as_dict_agent() for solicitude in solicitudes]
        return JSONResponse(solicitudes_dict)

    elif request.method == 'POST':
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

        if token == user.token:
            data = JSONParser().parse(request)
            # print(data)
            data['agent'] = user.id
            serializer = SolicitudeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                solicitude = Solicitude.objects.get(pk=serializer.data['id'])
                for item in data['items']:
                    Item(solicitude= solicitude, product= item['product'], amount= item['amount']).save()
                solicitudes = user.solicitude_set.all()
                solicitudes_dict = [solicitude.as_dict_agent() for solicitude in solicitudes]
                return JSONResponse(solicitudes_dict, status=201)
            print(serializer.errors)
            return JSONResponse(serializer.errors, status=400)
        else:
            return HttpResponse(status=401)

@csrf_exempt
def solicitude_detail(request, identifier, pk_solicitude):
    """
    Retrieve, update or delete a request.
    """
    try:
        user = Agent.objects.get(identifier=identifier)
        solicitude = user.solicitude_set.get(pk=pk_solicitude)
    except Agent.DoesNotExist:
        return HttpResponse(status=404)
    except Solicitude.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SolicitudeSerializer(solicitude)
        return JSONResponse(solicitude.as_dict_agent())
    elif request.method == 'DELETE':
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        if token == user.token:
            solicitude.change_to_closed()
            solicitudes = user.solicitude_set.all()
            solicitudes_dict = [solicitude.as_dict_agent() for solicitude in solicitudes]
            # photos = job_request.photo_set.all()
            # for photo in photos:
            #     simple_delete_job_request(photo)
            # job_request.delete()
            return JSONResponse(solicitudes_dict)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=404)























































API_KEY = '23e63458d588b10f67434ac7ca40b40e'
API_SECRET = '6108aa38fb2fa32124706e65af2b0c5c'
mailjet = Client(auth=(API_KEY, API_SECRET), version='v3')

def send_email(request):

    email = {
        'FromName': 'Mr Smith',
        'FromEmail': 'anthony.delpozo.m@gmail.com',
        'Subject': 'Test Email',
        'Text-Part': 'Hey there !',
        'Recipients': [{'Email': 'delan1997@gmail.com'}]
    }

    mailjet.send.create(email)
    return HttpResponse('')

def send_notification(request):
    headers = {
        'Authorization': 'key=AIzaSyB4ZBV-pbyLNYj_20lNI1czpfKGQ37ntrk',
        'Content-Type': 'application/json'
    }
    data = {
        'title':'Test',
        'body':'Hello world'
    }
    response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=data)
    content = response.content
    print(content)
    return HttpResponse('')
