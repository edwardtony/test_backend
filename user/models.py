from django.db import models
from django.forms.models import model_to_dict
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
# Create your models here.

class Agent(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=20, default="Apellido")
    email = models.EmailField(max_length=40, unique=True, error_messages= {'unique':"Este correo ya ha sido usado"})
    password = models.CharField(max_length=150)
    identifier = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=9, unique=True, error_messages= {'unique':"Este teléfono ya ha sido usado"})
    photo_url = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=175)
    code = models.CharField(max_length=10)
    fcm_token = models.CharField(max_length=200, blank=True)

    def as_dict_agent(self, solicitude = True, notification = True):
        result = model_to_dict(self, fields=None, exclude=['password','created_date'])
        if solicitude: result['solicitudes'] = [solicitude.as_dict_agent() for solicitude in Solicitude.objects.filter(closed=False, accepted=True, deadline__gte=datetime.now()).order_by('-id')]
        if notification: result['notifications'] = [notification.as_dict_agent() for notification in Notification.objects.filter(to__in = ["ALL", "AUT"]).order_by('-id')]
        return result

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password,self.password)

    def login(credentials):
        userTemp = Agent.objects.get(email=credentials['email'])
        result = userTemp.verify_password(credentials['password'])
        if result:
            return userTemp
        else:
            raise Agent.DoesNotExist
            return 0

    def __str__(self):
         return "Nombre: {} {} - Email: {}".format(self.name, self.last_name,self.email)

class EmpresaFocal(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=40, unique=True, error_messages= {'unique':"Este correo ya ha sido usado"})
    password = models.CharField(max_length=150)
    identifier = models.CharField(max_length=11)
    phone = models.CharField(max_length=9, unique=True, error_messages= {'unique':"Este teléfono ya ha sido usado"})
    photo_url = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=175)
    code = models.CharField(max_length=10)
    fcm_token = models.CharField(max_length=200, blank=True)

    def login(credentials):
        userTemp = EmpresaFocal.objects.get(email=credentials['email'])
        result = userTemp.verify_password(credentials['password'])
        if result:
            return userTemp
        else:
            raise EmpresaFocal.DoesNotExist
            return 0

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password,self.password)

    def as_dict_agent(self, solicitude = True, notification = True):
        result = model_to_dict(self, fields=None, exclude=['password'])
        if solicitude: result['solicitudes'] = [solicitude.as_dict_agent() for solicitude in Solicitude.objects.filter(closed=False, accepted=True, deadline__gte=datetime.now()).order_by('-id')]
        if notification: result['notifications'] = [notification.as_dict_agent() for notification in Notification.objects.filter(to__in = ["ALL", "PFO"]).order_by('-id')]
        return result

    def __str__(self):
         return "Nombre: {}".format(self.name)

class CodeAccount(models.Model):
    code = models.CharField(max_length=10, unique=True)
    image = models.CharField(max_length=30)
    used = models.BooleanField(default=False)

class Authority(models.Model):

    POSITION_OPTIONS = (
        ('1', 'Cargo 1'),
        ('2', 'Cargo 2'),
        ('3', 'Cargo 3'),
        ('4', 'Cargo 4'),
        ('5', 'Cargo 5')
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    position = models.CharField(max_length=1, choices=POSITION_OPTIONS)
    photo_url = models.CharField(max_length=100)

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        return result

    def __str__(self):
         return "Nombre: {} {}".format(self.first_name, self.last_name)

class Solicitude(models.Model):

    EMERGENCY_OPTIONS = (
        ('Sismo', 'Sismo'),
        ('Lluvia intensa', 'Lluvia intensa'),
        ('Inundación', 'Inundación'),
        ('Friaje', 'Friaje'),
        ('Huayco o deslizamiento', 'Huayco o deslizamiento')
    )

    PRIORITY_OPTIONS = (
        ('Prioridad 1', 'Prioridad 1'),
        ('Prioridad 2', 'Prioridad 2'),
        ('Prioridad 3', 'Prioridad 3'),
    )

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    emergency = models.CharField(max_length=30)
    district = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    region = models.CharField(max_length=40)
    priority = models.CharField(max_length=20, choices=PRIORITY_OPTIONS, blank=True)
    date = models.DateTimeField(default=datetime.now)
    deadline = models.DateTimeField(default=datetime.now() + timedelta(days=2))
    closed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    image_accepted = models.BooleanField(default=False)
    image_url = models.CharField(max_length=200, blank=True)

    receiver_name = models.CharField(max_length=30, blank=True)
    receiver_dni = models.CharField(max_length=8, blank=True)
    receiver_phone = models.CharField(max_length=9, blank=True)

    def change_to_closed(self):
        self.closed = True
        self.save()

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        result['agent'] = self.agent.as_dict_agent(False, False)
        result['authority'] = self.authority.as_dict_agent()
        result['product_list'] = [item.as_dict_agent() for item in self.item_set.all()]
        return result

    def __str__(self):
         return "Título: {} - Agente: {}  - Emergencia: {} - Fecha: {}".format(self.title, self.agent, self.emergency, self.date)

class Notification(models.Model):

    to = models.CharField(max_length=150)
    message = models.CharField(max_length=600)
    theme = models.CharField(max_length=20)
    solicitude = models.ForeignKey(Solicitude, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now)

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        if self.solicitude:
            result['solicitude'] = self.solicitude.as_dict_agent()
        return result

    def __str__(self):
         return "Para: {} - Tema: {}  - Solicitud: {} - Fecha: {}".format(self.to, self.theme, self.solicitude, self.date)

class Item(models.Model):

    solicitude = models.ForeignKey(Solicitude, on_delete=models.CASCADE)
    product = models.CharField(max_length=40)
    total = models.IntegerField()
    remaining = models.IntegerField()

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        result['helps'] = [help.as_dict_item() for help in self.help_set.all()]
        return result

    def __str__(self):
         return "Producto: {} - Total: {} - Faltan: {} - Petición: {}".format(self.product, self.total, self.remaining, self.solicitude)

class Photos(models.Model):

    solicitude = models.ForeignKey(Solicitude, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)

    def __str__(self):
        return "URL: {} - Petición: {}".format(self.url, self.solicitude)

class Help(models.Model):

    name = models.CharField(max_length=20)
    RUC_or_DNI = models.CharField(max_length=11)
    empresa_focal = models.ForeignKey(EmpresaFocal, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        return result

    def as_dict_item(self):
        result = model_to_dict(self, fields=["name", "amount"], exclude=None)
        return result

class HelpItem(models.Model):

    help = models.ForeignKey(Help, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        return result
