from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from rest_framework.parsers import JSONParser
from passlib.hash import pbkdf2_sha256
from django.http import HttpResponse
from django.conf import settings
from mailjet_rest import Client
from openpyxl import Workbook
from user.serializers import *
from user.models import *
from datetime import datetime, timedelta
import requests
import random
import json
import jwt

import os

import firebase_admin
from firebase_admin import credentials, messaging



# Create your views here.


#-------------------------------GLOBAL VARIABLES-------------------------------




cred = credentials.Certificate("/Users/anthonyedwarddelpozomatias/MEGAsync/geadapp-firebase-adminsdk-x2a5s-df26e617a9.json")
firebase_admin.initialize_app(cred)


message = messaging.Message(
    data={
        "title":"Hola desde el server",
        "body":"Soy el cuerpo de la notificación",
    },
    topic= "ALL",
)


# message = messaging.Message(
#     android=messaging.AndroidConfig(
#         ttl= timedelta(seconds=0),
#         priority='high',
#         data={
#             "title":"Hola desde el server",
#             "body":"Soy el cuerpo de la notificación",
#         }
#     ),
#     topic= "ALL",
# )

response = messaging.send(message)


print('Successfully sent message:', response)

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

def get_data_from_request(request):
    return request.POST.dict() if len(request.POST) else JSONParser().parse(request)


#--------------------------------------------- AGENT ---------------------------------------------

@csrf_exempt
def register(request):
    if request.method == 'POST':
        user = get_data_from_request(request)
        user['password'] = pbkdf2_sha256.encrypt(user['password'],rounds=12000,salt_size=32)
        user['identifier'] = generate_identifier()
        user['token'] = generate_token(user)

        serializer = AgentSerializer(data=user)

        if serializer.is_valid():
            try:
                validate_email(user['email'])
            except ValidationError as e:
                return JSONResponse(e, status=404)
            serializer.save()
            user_return = Agent.objects.get(pk= serializer.data['id'])
            return JSONResponse(user_return.as_dict_agent(), status=201)
        return JSONResponse({'error':{'code': 401, 'message':'Este correo ya ha sido usado'}})
    return JSONResponse({'error':{'code': 405, 'message':'Método Http incorrecto'}})

@csrf_exempt
def login(request):
    print("Login")

    if request.method == 'POST':
        credentials = get_data_from_request(request)
        print("credentials", credentials)
        try:
            user = Agent.login(credentials)
            token = user.token
            print("USER", token)
            return JSONResponse({'token':token})
        except Agent.DoesNotExist as e:
            print(e)

        print(credentials)
        try:
            focal = EmpresaFocal.login(credentials)
            token = focal.token
            print("FOCAL", token)
            return JSONResponse({'token':token})
        except EmpresaFocal.DoesNotExist as e:
            print(e)

        print("HI")
        return JSONResponse({'error':{'code': 401, 'message':'Correo o contraseña incorrecto'}})
    return JSONResponse({'error':{'code': 405, 'message':'Método Http incorrecto'}})

@csrf_exempt
def user_info(request):
    if request.method == 'GET':
        if 'HTTP_AUTHORIZATION' not in request.META: return JSONResponse({'error':{'code': 403, 'message':'Error de autorización'}}, status=403)
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        print(token)
        try:
            agent = Agent.objects.get(token=token)
            print("USER", agent)
            return JSONResponse({'login':{'agent':agent.as_dict_agent()}})
        except Exception as e:
            print(e)

        try:
            focal = EmpresaFocal.objects.get(token=token)
            print("FOCAL", focal)
            return JSONResponse({'login':{'focal':focal.as_dict_agent()}})
        except Exception as e:
            print(e)

        return JSONResponse({'error':{'code': 401, 'message':'Correo o contraseña incorrecto'}}, status=401)
    else:
        return JSONResponse({'error':{'code': 405, 'message':'Método Http incorrecto'}}, status=405)



#---------------------------------SOLICITUDE-------------------------------------
@csrf_exempt
def donate(request, identifier):
    """
    List all code request, or create a new request.
    """
    try:
        user = Agent.objects.get(identifier=identifier)
    except Agent.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'POST':
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

        if token == user.token:
            data = get_data_from_request(request)
            return JSONResponse({}, status=201)

        #     print(data)
        #     data['agent'] = user.id
        #     # data['date'] = "2018-10-30T04:05"
        #     # data['deadline'] = "2018-11-1T04:05"
        #     serializer = SolicitudeSerializer(data=data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         solicitude = Solicitude.objects.get(pk=serializer.data['id'])
        #         if 'items' in data:
        #             for item in json.loads(request.POST.dict()['items']):
        #                 Item(solicitude= solicitude, product= item['product'], amount= item['amount']).save()
        #         if 'product_list' in data:
        #             for item in json.loads(request.POST.dict()['product_list']):
        #                 Item(solicitude= solicitude, product= item['product'], amount= item['amount']).save()
        #         solicitudes = Solicitude.objects.filter(closed=False, accepted=True, deadline__gte=datetime.now()).order_by('-id')
        #         solicitudes_dict = [solicitude.as_dict_agent() for solicitude in solicitudes]
        #         return JSONResponse({'solicitudes':solicitudes_dict}, status=201)
        #     print(serializer.errors)
            return JSONResponse(serializer.errors, status=400)
        else:
            return HttpResponse(status=401)

    else:
        return HttpResponse(status=405)

#---------------------------------SOLICITUDE-------------------------------------
@csrf_exempt
def solicitude_list(request, identifier):
    """
    List all code request, or create a new request.
    """
    print("HI")

    if request.method == 'GET':
        solicitudes = Solicitude.objects.filter(closed=False, accepted=True, deadline__gte=datetime.now()).order_by('-id')
        solicitudes_dict = [solicitude.as_dict_agent() for solicitude in solicitudes]
        return JSONResponse({'solicitudes':solicitudes_dict})

    elif request.method == 'POST':
        try:
            user = Agent.objects.get(identifier=identifier)
        except Agent.DoesNotExist:
            return JSONResponse({'error':{'code': 403, 'message':'Error de autorización'}}, status=403)
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

        if token == user.token:
            data = get_data_from_request(request)
            data['agent'] = user.id
            # data['date'] = "2018-10-30T04:05"
            # data['deadline'] = "2018-11-1T04:05"
            serializer = SolicitudeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                solicitude = Solicitude.objects.get(pk=serializer.data['id'])
                if 'product_list' in data:
                    for item in json.loads(request.POST.dict()['product_list']):
                        Item(solicitude= solicitude, product= item['product'], amount= item['amount']).save()
                solicitudes = Solicitude.objects.filter(closed=False, accepted=True, deadline__gte=datetime.now()).order_by('-id')
                solicitudes_dict = [solicitude.as_dict_agent() for solicitude in solicitudes]

                send_email("SOLICITUD CREADA", solicitude)
                return JSONResponse({'solicitudes':solicitudes_dict}, status=201)
            return JSONResponse({'error':{'code': 401, 'message':'Datos no válidos '}})
        else:
            return JSONResponse({'error':{'code': 401, 'message':'Correo o contraseña incorrecto'}})
    else:
        return JSONResponse({'error':{'code': 405, 'message':'Método Http incorrecto'}})

from django.http import QueryDict

@csrf_exempt
def solicitude_detail(request, identifier, pk_solicitude):
    """
    Retrieve, update or delete a request.
    """
    try:
        solicitude = Solicitude.objects.get(pk=pk_solicitude)
    except Agent.DoesNotExist:
        return HttpResponse(status=404)
    except Solicitude.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        #serializer = SolicitudeSerializer(solicitude)
        print("SOLICITUDE", solicitude.as_dict_agent())
        return JSONResponse({'solicitude':solicitude.as_dict_agent()})
    elif request.method == 'DELETE':
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        solicitude.change_to_closed()
        solicitudes = user.solicitude_set.all()
        solicitudes_dict = [solicitude.as_dict_agent() for solicitude in solicitudes]
        # photos = job_request.photo_set.all()
        # for photo in photos:
        #     simple_delete_job_request(photo)
        # job_request.delete()
        return JSONResponse(solicitudes_dict)
    elif request.method == 'PUT':
        delete_item = True
        data = QueryDict(request.body)
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        solicitude = Solicitude.objects.filter(pk=pk_solicitude).first()
        solicitude_temp = Solicitude.objects.get(pk=solicitude.pk)

        focal = Focal(name=data['name'], RUC_or_DNI=data['ruc_or_dni'])
        focal.save()
        solicitude.focal = focal
        solicitude.closed = True
        solicitude.save()
        solicitude.focal = None
        solicitude.pk = None
        solicitude.closed = False
        solicitude.save()

        data = QueryDict(request.body)

        amount_list = json.loads(data['product_list'])
        for (index, item) in enumerate(Solicitude.objects.get(pk=solicitude_temp.pk).item_set.all()):
            print(index)
            item.help = amount_list[index]
            item.save()
            item.pk = None
            item.amount = item.amount - amount_list[index]
            if item.amount != 0:
                delete_item = False
                item.help = 0
                item.solicitude = solicitude
                item.save()

        if delete_item:
            solicitude.delete()
        send_email("DONACIÓN REALIZADA", solicitude)
        return JSONResponse({}, status=200)
    else:
        return JSONResponse({'error':{'code': 405, 'message':'Método Http incorrecto'}}, status=405)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES['upload']:
        image = request.FILES['upload']
        fs = FileSystemStorage()
        path = str(random.randint(0,9999999999)) + ".png"
        filename = fs.save(path, image)
        print(filename)
        return JSONResponse({'image_url': filename}, status=201)
    return JSONResponse({'error':{'code': 405, 'message':'Método Http incorrecto'}}, status=405)

#---------------------------------EXCEL-------------------------------------
@csrf_exempt
def export_excel(request):
    if request.method == 'GET':
        solicitudes = Solicitude.objects.all()
        wb = Workbook()
        ws = wb.active
        ws['B2'] = "REPORTE DE SOLICITUDES"
        ws.merge_cells('B2:J2')

#GEAD
        ws['B4'] = "Código"
        ws['C4'] = "Agente"
        ws['D4'] = "Autoridad"
        ws['E4'] = "Título"
        ws['F4'] = "Emergencia"
        ws['G4'] = "Distrito"
        ws['H4'] = "Provincia"
        ws['I4'] = "Región"
        ws['J4'] = "Magnitud"
        ws['K4'] = "Fecha"

        start_index = 5
        file_name = "ReporteSolicitudes {0}.xlsx".format(datetime.now().strftime("%d/%m/%y %H:%M"))

        for solicitude in solicitudes:
            ws.cell(row=start_index, column=2).value = "#GEAD" + str(solicitude.pk)
            ws.cell(row=start_index, column=3).value = solicitude.agent.first_name
            ws.cell(row=start_index, column=4).value = solicitude.authority.first_name
            ws.cell(row=start_index, column=5).value = solicitude.title
            ws.cell(row=start_index, column=6).value = solicitude.emergency
            ws.cell(row=start_index, column=7).value = solicitude.district
            ws.cell(row=start_index, column=8).value = solicitude.province
            ws.cell(row=start_index, column=9).value = solicitude.region
            ws.cell(row=start_index, column=10).value = solicitude.priority
            ws.cell(row=start_index, column=11).value = solicitude.date.strftime('%d/%m/%y')
            start_index+=1
            for item in solicitude.item_set.all():
                ws.cell(row=start_index, column=3).value = item.pk
                ws.cell(row=start_index, column=4).value = item.product
                ws.cell(row=start_index, column=5).value = item.amount
                start_index+=1

        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(file_name)
        response['Content-Disposition'] = content
        wb.save(response)
        return response



#---------------------------------PASSWORD-------------------------------------
@csrf_exempt
def forgotten_password(request):
    if request.method == 'POST':
        data = get_data_from_request(request)
        send_email("Se ha enviado un correo a {} para que reinicie su cuenta".format(data['email']), None)
        return JSONResponse({},status=200)
    return JSONResponse({'error':{'code': 405, 'message':'Método Http incorrecto'}}, status=405)


































API_KEY = '23e63458d588b10f67434ac7ca40b40e'
API_SECRET = '6108aa38fb2fa32124706e65af2b0c5c'
mailjet = Client(auth=(API_KEY, API_SECRET), version='v3')

def send_email(message, solicitude):

    email = {
        'FromName': 'GEAD APP',
        'FromEmail': 'anthony.delpozo.m@gmail.com',
        'Subject': message,
        'Text-Part': message,
        'Recipients': [{'Email': 'delan1997@gmail.com'}]
    }

    message = messaging.Message(
        data={
            "title":"GEAD APP",
            "body":message,
            "solicitude_id": str(solicitude.pk),
        },
        topic= "ALL",
    )

    response = messaging.send(message)

    #mailjet.send.create(email)
    # return HttpResponse('')

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
