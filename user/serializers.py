from rest_framework import serializers
from .models import *

class AgentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Agent
		fields = '__all__'

        
class AuthoritySerializer(serializers.ModelSerializer):
	class Meta:
		model = Authority
		fields = '__all__'

        
class SolicitudeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Solicitude
		fields = '__all__'

        
class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = '__all__'

        
class PhotosSerializer(serializers.ModelSerializer):
	class Meta:
		model = Photos
		fields = '__all__'

