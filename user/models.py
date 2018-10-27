from django.db import models
from django.forms.models import model_to_dict
from passlib.hash import pbkdf2_sha256

# Create your models here.

class Agent(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40, unique=True)
    password = models.CharField(max_length=150)
    identifier = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=9, unique=True)
    photo_url = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=175)

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=['password','created_date','token'])
        result['requests'] = [request.as_dict_user() for request in self.request_set.filter()]
        return result

    def verify_password(self, password):
    		return pbkdf2_sha256.verify(password,self.password)

    def login(credentials):
        userTemp = Agent.objects.get(email=credentials['email'])
        result = userTemp.verify_password(credentials['password'])
        if result:
            return userTemp
        else:
            raise User.DoesNotExist
            return 0

    def __str__(self):
         return "Nombre: {} {} - Email: {}".format(self.first_name, self.last_name,self.email)

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

class Request(models.Model):

    EMERGENCY_OPTIONS = (
        ('1', 'Emergencia 1'),
        ('2', 'Emergencia 2'),
        ('3', 'Emergencia 3'),
        ('4', 'Emergencia 4'),
        ('5', 'Emergencia 5')
    )

    DISTRICT_OPTIONS = (
        ('1', 'Distrito 1'),
        ('2', 'Distrito 2'),
        ('3', 'Distrito 3'),
        ('4', 'Distrito 4'),
        ('5', 'Distrito 5')
    )

    PROVINCE_OPTIONS = (
        ('1', 'Provincia 1'),
        ('2', 'Provincia 2'),
        ('3', 'Provincia 3'),
        ('4', 'Provincia 4'),
        ('5', 'Provincia 5')
    )

    REGION_OPTIONS = (
        ('1', 'Región 1'),
        ('2', 'Región 2'),
        ('3', 'Región 3'),
        ('4', 'Región 4'),
        ('5', 'Región 5')
    )

    MAGNITUDE_OPTIONS = (
        ('1', 'Magnitud 1'),
        ('2', 'Magnitud 2'),
        ('3', 'Magnitud 3'),
        ('4', 'Magnitud 4'),
        ('5', 'Magnitud 5')
    )

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    emergency = models.CharField(max_length=1, choices=EMERGENCY_OPTIONS)
    district = models.CharField(max_length=1, choices=DISTRICT_OPTIONS)
    province = models.CharField(max_length=1, choices=PROVINCE_OPTIONS)
    region = models.CharField(max_length=1, choices=REGION_OPTIONS)
    magnitude = models.CharField(max_length=1, choices=MAGNITUDE_OPTIONS)
    date = models.DateField(auto_now_add=True)

    def as_dict_agent(self):
        result = model_to_dict(self, fields=None, exclude=None)
        result['authority'] = self.authority.as_dict_agent()
        return result

    def __str__(self):
         return "Agente: {} - Autoridad: {} - Emergencia: {} - Fecha: {}".format(self.agent, self.authority, self.emergency, self.date)

class Item(models.Model):

    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    product = models.CharField(max_length=20)
    amount = models.IntegerField()

    def __str__(self):
         return "Producto: {} - Cantidad: {} - Petición: {}".format(self.product, self.amount, self.request)

class Photos(models.Model):

    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)

    def __str__(self):
            return "URL: {} - Petición: {}".format(self.url, self.request)
