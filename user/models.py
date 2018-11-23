from django.db import models
from django.forms.models import model_to_dict
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
# Create your models here.

class Agent(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40, unique=True, error_messages= {'unique':"Este correo ya ha sido usado"})
    password = models.CharField(max_length=150)
    identifier = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=9, unique=False, error_messages= {'unique':"Este teléfono ya ha sido usado"})
    photo_url = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=175)

    def as_dict_agent(self, solicitude = True):
        result = model_to_dict(self, fields=None, exclude=['password','created_date'])
        if solicitude: result['solicitudes'] = [solicitude.as_dict_agent() for solicitude in Solicitude.objects.filter(closed=False, accepted=True, deadline__gte=datetime.now()).order_by('-id')]
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
         return "Nombre: {} {} - Email: {}".format(self.first_name, self.last_name,self.email)

class Focal(models.Model):

    name = models.CharField(max_length=20)
    RUC_or_DNI = models.CharField(max_length=11)

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        return result

    def __str__(self):
         return "Nombre: {} {}".format(self.name, self.RUC_or_DNI)

class EmpresaFocal(models.Model):

    name = models.CharField(max_length=20)
    RUC_or_DNI = models.CharField(max_length=11)
    identifier = models.CharField(max_length=11)
    token = models.CharField(max_length=175)
    phone = models.CharField(max_length=9, unique=False, error_messages= {'unique':"Este teléfono ya ha sido usado"})
    photo_url = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=40, unique=True, error_messages= {'unique':"Este correo ya ha sido usado"})
    password = models.CharField(max_length=150)

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

    def as_dict_agent(self, solicitude = True):
        result = model_to_dict(self, fields=None, exclude=['password'])
        if solicitude: result['solicitudes'] = [solicitude.as_dict_agent() for solicitude in Solicitude.objects.filter(closed=False, accepted=True, deadline__gte=datetime.now()).order_by('-id')]
        return result

    def __str__(self):
         return "Nombre: {} {}".format(self.name, self.RUC_or_DNI)


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
        ('Emergencia 1', 'Emergencia 1'),
        ('Emergencia 2', 'Emergencia 2'),
        ('Emergencia 3', 'Emergencia 3'),
        ('Emergencia 4', 'Emergencia 4'),
        ('Emergencia 5', 'Emergencia 5')
    )

    DISTRICT_OPTIONS = (
        ('Distrito 1', 'Distrito 1'),
        ('Distrito 2', 'Distrito 2'),
        ('Distrito 3', 'Distrito 3'),
        ('Distrito 4', 'Distrito 4'),
        ('Distrito 5', 'Distrito 5')
    )

    PROVINCE_OPTIONS = (
        ('Provincia 1', 'Provincia 1'),
        ('Provincia 2', 'Provincia 2'),
        ('Provincia 3', 'Provincia 3'),
        ('Provincia 4', 'Provincia 4'),
        ('Provincia 5', 'Provincia 5')
    )

    REGION_OPTIONS = (
        ('Región 1', 'Región 1'),
        ('Región 2', 'Región 2'),
        ('Región 3', 'Región 3'),
        ('Región 4', 'Región 4'),
        ('Región 5', 'Región 5')
    )

    PRIORITY_OPTIONS = (
        ('Prioridad 1', 'Prioridad 1'),
        ('Prioridad 2', 'Prioridad 2'),
        ('Prioridad 3', 'Prioridad 3'),
        ('Prioridad 4', 'Prioridad 4'),
        ('Prioridad 5', 'Prioridad 5')
    )

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    focal = models.ForeignKey(Focal, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=30)
    emergency = models.CharField(max_length=20, choices=EMERGENCY_OPTIONS)
    district = models.CharField(max_length=20, choices=DISTRICT_OPTIONS)
    province = models.CharField(max_length=20, choices=PROVINCE_OPTIONS)
    region = models.CharField(max_length=20, choices=REGION_OPTIONS)
    priority = models.CharField(max_length=20, choices=PRIORITY_OPTIONS, blank=True)
    date = models.DateTimeField(default=datetime.now)
    deadline = models.DateTimeField(default=datetime.now() + timedelta(days=2))
    closed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    image_accepted = models.BooleanField(default=False)
    image_url = models.CharField(max_length=200, blank=True)

    def change_to_closed(self):
        self.closed = True
        self.save()

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        result['agent'] = self.agent.as_dict_agent(False)
        result['authority'] = self.authority.as_dict_agent()
        if self.focal :
            result['focal'] = self.focal.as_dict_agent()
        result['product_list'] = [item.as_dict_agent() for item in self.item_set.all()]
        return result

    def __str__(self):
         return "Agente: {} - Autoridad: {} - Emergencia: {} - Fecha: {}".format(self.agent, self.authority, self.emergency, self.date)

class Item(models.Model):

    solicitude = models.ForeignKey(Solicitude, on_delete=models.CASCADE)
    product = models.CharField(max_length=40)
    amount = models.IntegerField()
    help = models.IntegerField(blank=True, null=True)

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        return result

    def __str__(self):
         return "Producto: {} - Cantidad: {} - Petición: {}".format(self.product, self.amount, self.solicitude)

class Photos(models.Model):

    solicitude = models.ForeignKey(Solicitude, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)

    def __str__(self):
            return "URL: {} - Petición: {}".format(self.url, self.solicitude)
